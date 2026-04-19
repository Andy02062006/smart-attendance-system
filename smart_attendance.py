import cv2, face_recognition, numpy as np, requests, os
from datetime import datetime
from scipy.spatial import distance as dist

def get_ear(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def get_mar(mouth):
    A = dist.euclidean(mouth[2], mouth[10]) # Top and bottom lip inner
    B = dist.euclidean(mouth[4], mouth[8])
    C = dist.euclidean(mouth[0], mouth[6]) # Left and right corners
    return (A + B) / (2.0 * C)

# Setup
KNOWN = {"Andrea": "Andrea.jpg", "Aishwarya": "Aishwarya.jpg"}
encodings, names = [], []
for n, f in KNOWN.items():
    if os.path.exists(f):
        encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(f))[0])
        names.append(n)

video = cv2.VideoCapture(0)
last_alert = {}
drowsy_frames = {} # Track consecutive frames eyes are closed
drowsy_start_time = {} # Track when student first became drowsy
marked_today_local = set() # Prevent redundant API calls in same session
EYE_AR_THRESH = 0.25 # Increased for higher sensitivity
EYE_AR_CONSEC_FRAMES = 10 # Decreased to trigger faster on slow hardware

while True:
    ret, frame = video.read()
    if not ret: continue
    
    # Optimization: Resize frame to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    locs = face_recognition.face_locations(rgb)
    all_landmarks = face_recognition.face_landmarks(rgb, locs)
    encs = face_recognition.face_encodings(rgb, locs)

    for loc, landmarks, enc in zip(locs, all_landmarks, encs):
        ear = (get_ear(landmarks['left_eye']) + get_ear(landmarks['right_eye'])) / 2.0
        mar = get_mar(landmarks['top_lip'] + landmarks['bottom_lip'])
        
        dist_val = face_recognition.face_distance(encodings, enc)
        name = "Unknown"
        if len(dist_val) > 0 and np.min(dist_val) < 0.5:
            name = names[np.argmin(dist_val)]

        engagement = "Active"
        if ear < EYE_AR_THRESH:
            drowsy_frames[name] = drowsy_frames.get(name, 0) + 1
            if drowsy_frames[name] >= EYE_AR_CONSEC_FRAMES:
                engagement = "Drowsy"
                if name not in drowsy_start_time:
                    drowsy_start_time[name] = datetime.now()
        else:
            drowsy_frames[name] = 0
            drowsy_start_time.pop(name, None)
            if mar > 0.5:
                engagement = "Distracted"

        # Check for Severe Alert (2 minutes)
        if name != "Unknown" and name in drowsy_start_time:
            duration = (datetime.now() - drowsy_start_time[name]).total_seconds()
            if duration > 120:
                engagement = "CRITICAL: SLEEPING"
        
        if name != "Unknown":
            # Send live detection info
            try:
                requests.post("http://localhost:8080/api/detect", 
                              json={"name": name, "time": datetime.now().strftime("%H:%M:%S"), 
                                    "status": "Present", "engagement": engagement}, timeout=0.1)
                
                # Auto-mark attendance once per session/day
                if name not in marked_today_local:
                    requests.post("http://localhost:8080/api/attendance", 
                                  json={"name": name, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                        "status": "Present", "engagement": engagement}, timeout=0.1)
                    marked_today_local.add(name)
                
                # Send Alert (Throttled or on critical state change)
                now = datetime.now()
                is_critical = "CRITICAL" in engagement
                throttle_time = 2 if is_critical else 10 # More frequent if critical
                
                if engagement != "Active":
                    if name not in last_alert or (now - last_alert[name]).total_seconds() > throttle_time:
                        requests.post("http://localhost:8080/api/alerts", 
                                      json={"name": name, "status": engagement, "time": now.strftime("%H:%M:%S")}, timeout=0.1)
                        last_alert[name] = now
            except: pass

        # Scale back up locations for drawing
        top, right, bottom, left = [v * 4 for v in loc]
        color = (0, 0, 255) if "CRITICAL" in engagement else (0, 255, 255) if engagement == "Drowsy" else (0, 255, 0) if engagement == "Active" else (255, 255, 0)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, f"{name}: {engagement}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("SmartSense Monitor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

video.release()
cv2.destroyAllWindows()