import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os
import sys

# Constants
CSV_FILE = "attendance.csv"
TOLERANCE = 0.5
KNOWN_FACES = {
    "Andrea": "Andrea.jpg",
    "Aishwarya": "Aishwarya.jpg"
}

print("--- Smart Attendance System Starting ---")
print("Loading known faces...")

known_face_encodings = []
known_face_names = []

for name, filename in KNOWN_FACES.items():
    if not os.path.exists(filename):
        print(f"Warning: Image file not found for {name}: {filename}")
        continue
    try:
        image = face_recognition.load_image_file(filename)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            print(f"Loaded {name}")
        else:
            print(f"Warning: No face found in {filename}")
    except Exception as e:
        print(f"Error loading {filename}: {e}")

if not known_face_names:
    print("Error: No faces loaded. Exiting.")
    sys.exit(1)

# Initialize CSV if not exists
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Name", "Time"]).to_csv(CSV_FILE, index=False)

# Load today's marked names to prevent duplicates
today_date = datetime.now().strftime("%Y-%m-%d")
try:
    df = pd.read_csv(CSV_FILE)
    today_marked = set(df[df['Time'].str.startswith(today_date)]["Name"].tolist())
    print(f"Already marked today: {', '.join(today_marked) if today_marked else 'None'}")
except Exception as e:
    print(f"Error reading CSV: {e}")
    today_marked = set()

print("Starting camera (AVFoundation)...")
video_capture = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not video_capture.isOpened():
    print("Error: Could not open camera. Please check permissions.")
    sys.exit(1)

print("Press 'q' in the camera window to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame. Retrying...")
        continue
    
    # Process smaller frame for speed
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, TOLERANCE)
        name = "Unknown"
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # MARK ATTENDANCE (Strictly once per day)
        if name != "Unknown" and name not in today_marked:
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                # Append to CSV
                new_entry = pd.DataFrame([[name, time_now]], columns=["Name", "Time"])
                new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)
                
                today_marked.add(name)
                print(f"SUCCESS: Marked attendance for {name} at {time_now}")
            except Exception as e:
                print(f"Error writing attendance: {e}")

        # Draw box and name
        top, right, bottom, left = top*4, right*4, bottom*4, left*4
        cv2.rectangle(frame, (left, top), (right, bottom), (99, 102, 241), 2) # Modern color (indigo-ish)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (99, 102, 241), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    cv2.imshow("Smart Attendance - Scanning...", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
print("Camera closed.")