package attendance.controller;

import attendance.model.Attendance;
import attendance.service.CSVService;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;
import java.util.*;

@Controller
@RestController // Combine for simplicity
@RequestMapping("/api")
public class AttendanceController {

    @GetMapping("/") // Redirect from root
    public String home() { return "redirect:/login.html"; }

    @GetMapping("/attendance")
    public List<Attendance> get() { return CSVService.getAttendance(); }

    @GetMapping("/download")
    public org.springframework.core.io.Resource download() {
        return new org.springframework.core.io.FileSystemResource("attendance.csv");
    }

    @PostMapping("/attendance")
    public Attendance mark(@RequestBody Attendance a) {
        CSVService.saveAttendance(a);
        return a;
    }

    @PostMapping("/open-camera")
    public Map<String, String> camera() {
        try {
            new ProcessBuilder("python3", "smart_attendance.py").start();
            return Collections.singletonMap("status", "success");
        } catch (Exception e) {
            return Collections.singletonMap("status", "error");
        }
    }

    @GetMapping("/logout")
    public String logout() { return "redirect:/login.html"; }
}