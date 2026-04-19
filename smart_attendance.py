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
while True:
    ret, frame = video.read()
    if not ret: continue
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locs = face_recognition.face_locations(rgb)
    all_landmarks = face_recognition.face_landmarks(rgb, locs)
    encs = face_recognition.face_encodings(rgb, locs)

    for loc, landmarks, enc in zip(locs, all_landmarks, encs):
        # Calculate Engagement
        ear = (get_ear(landmarks['left_eye']) + get_ear(landmarks['right_eye'])) / 2.0
        mar = get_mar(landmarks['top_lip'] + landmarks['bottom_lip'])
        
        engagement = "Active"
        if ear < 0.22: engagement = "Drowsy"
        elif mar > 0.5: engagement = "Distracted" # Simplified: Yawning or talking too much

        dist_val = face_recognition.face_distance(encodings, enc)
        name = "Unknown"
        if len(dist_val) > 0 and np.min(dist_val) < 0.5:
            name = names[np.argmin(dist_val)]
            requests.post("http://localhost:8080/api/attendance", 
                          json={
                              "name": name, 
                              "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              "status": "Present",
                              "engagement": engagement
                          })

        top, right, bottom, left = loc
        color = (0, 255, 0) if engagement == "Active" else (0, 255, 255) if engagement == "Drowsy" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, f"{name}: {engagement}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("SmartSense Pro: AI Analysis", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

video.release()
cv2.destroyAllWindows()