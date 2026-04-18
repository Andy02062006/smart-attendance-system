import cv2, face_recognition, numpy as np, requests, os
from datetime import datetime

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
    
    small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    
    locs = face_recognition.face_locations(rgb)
    encs = face_recognition.face_encodings(rgb, locs)

    for loc, enc in zip(locs, encs):
        dist = face_recognition.face_distance(encodings, enc)
        name = "Unknown"
        if len(dist) > 0 and np.min(dist) < 0.5:
            name = names[np.argmin(dist)]
            # SRS: Mark with "Active" engagement
            requests.post("http://localhost:8080/api/attendance", 
                          json={"name": name, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "engagement": "Active"})

        top, right, bottom, left = [v * 4 for v in loc]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

video.release()
cv2.destroyAllWindows()