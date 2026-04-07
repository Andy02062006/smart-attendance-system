import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os

print("Loading known faces...")

known_face_encodings = []
known_face_names = []

image = face_recognition.load_image_file("Andrea.jpg")
encodings = face_recognition.face_encodings(image)
if len(encodings) == 0:
    print("Error: No face found in Andrea.jpg")
    exit()
known_face_encodings.append(encodings[0])
known_face_names.append("Andrea")

image = face_recognition.load_image_file("Aishwarya.jpg")
encodings = face_recognition.face_encodings(image)
if len(encodings) == 0:
    print("Error: No face found in Aishwarya.jpg")
    exit()
known_face_encodings.append(encodings[0])
known_face_names.append("Aishwarya")

print("Faces loaded successfully!")

if not os.path.exists("attendance.csv"):
    pd.DataFrame(columns=["Name", "Time"]).to_csv("attendance.csv", index=False)

print("Starting camera...")

video_capture = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
if not video_capture.isOpened():
    print("Error: Camera not accessible")
    exit()

print("Press 'q' to quit")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    today_date = datetime.now().strftime("%Y-%m-%d")
    attendance_df = pd.read_csv("attendance.csv")
    today_df = attendance_df[attendance_df['Time'].str.startswith(today_date)]
    today_names = today_df["Name"].tolist()

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding, tolerance=0.5
        )
        name = "Unknown"
        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding
        )

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        if name != "Unknown" and name not in today_names:
            now = datetime.now()
            time = now.strftime("%Y-%m-%d %H:%M:%S")
            df = pd.DataFrame([[name, time]], columns=["Name", "Time"])
            df.to_csv("attendance.csv", mode='a', header=False, index=False)
            print(f"{name} marked present at {time}")
            today_names.append(name)  
            
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()