# SmartSense: Smart Attendance & Engagement System

SmartSense is an AI-based facial recognition and IoT system designed to automate attendance marking and providing real-time engagement insights.

## Project Architecture (MVC)

The project follows the **Model-View-Controller (MVC)** design pattern to ensure clear separation of concerns:

- **Model**: Located in `attendance.model`. Contains `AttendanceRecord.java` which defines the data structure for student attendance and engagement metrics.
- **View**: Located in `src/main/resources/static`. Uses `index.html` for the dashboard UI, displaying real-time metrics and records.
- **Controller**: Located in `attendance.controller`. `AttendanceController.java` manages API requests, triggers the AI script, and coordinates between the View and the Model services.

## Spring Boot Structure

Built on the **Spring Boot** framework, the project utilizes:
- **RESTful APIs**: Exposing endpoints for marking attendance and fetching data.
- **Static Content Hosting**: Serving the dashboard directly from the `resources/static` directory.
- **Dependency Injection**: Managing services and controllers for a scalable backend.

## AI & IoT Integration

- **Face Recognition**: A Python-based `smart_attendance.py` script uses the `face_recognition` library and OpenCV to detect and identify registered students.
- **Data Persistence**: Attendance and engagement data are stored in a centralized `attendance.csv` file, managed by the `CSVService` for easy export and reporting.

---

## How to Run

1.  **Backend**: Run `./mvnw spring-boot:run` in the project root.
2.  **Dashboard**: Open `http://localhost:8080` in your browser.
3.  **Recognition**: Click "Face Recognition & Analysis" on the dashboard to start marking attendance.