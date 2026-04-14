package attendance;

import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;
import java.util.*;

@Controller
public class AttendanceController {

    @GetMapping("/")
    public String redirectToLogin() {
        return "redirect:/login.html";
    }

    @RestController
    @RequestMapping("/api")
    public static class AttendanceAPI {
        
        @GetMapping("/attendance")
        public List<Attendance> getAttendance() {
            return CSVService.getAttendance();
        }

        @PostMapping("/attendance")
        public Attendance markAttendance(@RequestBody Attendance attendance) {
            CSVService.saveAttendance(attendance);
            return attendance;
        }

        @PostMapping("/open-camera")
        public Map<String, String> openCamera() {
            Map<String, String> response = new HashMap<>();
            try {
                // Call the python script and inherit IO so output shows in console
                ProcessBuilder pb = new ProcessBuilder("python3", "smart_attendance.py");
                pb.inheritIO(); 
                pb.start();
                response.put("status", "success");
                response.put("message", "Camera opened successfully");
                System.out.println("Starting smart_attendance.py...");
            } catch (Exception e) {
                System.err.println("Failed to start camera process: " + e.getMessage());
                response.put("status", "error");
                response.put("message", e.getMessage());
            }
            return response;
        }
    }

    @GetMapping("/logout")
    public String logout() {
        return "redirect:/login.html";
    }
}