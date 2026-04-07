package attendance;

import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import java.util.*;

@Controller
public class AttendanceController {

    @GetMapping("/")
    public String redirectToLogin() {
        return "redirect:/login.html";
    }

    @GetMapping("/index.html")
    public String getDashboard(Model model) {
        // Check if user is authenticated (you can add JWT verification here)
        return "index";
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
    }
}