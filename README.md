# SmartSense Pro: Intelligent Attendance & Engagement

SmartSense Pro is a premium, AI-powered system designed for modern classrooms. It automates attendance through facial recognition and provides real-time insights into student engagement, including drowsiness and distraction monitoring.

## Professional Features

### 1. Role-Based Dashboards
The system provides tailored experiences for different users:
- **Admin**: System-wide controls, data reset, and full reporting.
- **Teacher**: Lecture initiation, real-time engagement analytics, and secure lecture recording.
- **Student**: Personal attendance tracking and engagement history.

### 2. AI-Driven Engagement Monitoring
Beyond simple attendance, SmartSense Pro uses facial landmarks to track student focus:
- **Active Focus**: Real-time tracking of presence and attention.
- **Drowsiness Detection**: Monitors Eye Aspect Ratio (EAR) to detect signs of fatigue.
- **Distraction Alerts**: Calculates Mouth Aspect Ratio (MAR) to detect yawning or excessive talking.

### 3. Integrated Lecture Recording
Faculty can record their screens and lectures directly from the dashboard, ensuring educational content is preserved for future review.

### 4. Professional Analytics
Real-time doughnut charts and visual metrics provide an immediate overview of classroom dynamics.

---

## Technical Architecture (MVC)

- **Model**: `AttendanceRecord.java` manages data structures for attendance and engagement.
- **View**: A sophisticated, glassmorphism-inspired frontend using HTML5, CSS3, and Chart.js.
- **Controller**: `AttendanceController.java` routes requests and coordinates AI script triggers.

---

## How to Run

1.  **Backend**: Run `./mvnw spring-boot:run` in the project root.
2.  **AI System**: Ensure requirements are installed via `pip install -r requirements.txt`.
3.  **Dashboard**: Access `http://localhost:8080`.
4.  **Login**: Choose your role. Use any non-empty credentials for demo purposes.
5.  **Operation**: Teachers can start AI Analysis and Lecture Recording from their respective panels.