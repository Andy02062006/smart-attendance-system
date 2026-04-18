package attendance.controller;

import attendance.model.AttendanceRecord;
import attendance.service.CSVService;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;
import java.util.*;

@Controller
@RestController
@RequestMapping("/api")
public class AttendanceController {

    @GetMapping("/")
    public String home() { return "redirect:/login.html"; }

    @GetMapping("/attendance")
    public List<AttendanceRecord> get() { return CSVService.getAttendance(); }

    @GetMapping("/download")
    public org.springframework.http.ResponseEntity<org.springframework.core.io.Resource> download() {
        org.springframework.core.io.Resource file = new org.springframework.core.io.FileSystemResource("attendance.csv");
        return org.springframework.http.ResponseEntity.ok()
            .header(org.springframework.http.HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"attendance_report.csv\"")
            .header(org.springframework.http.HttpHeaders.CONTENT_TYPE, "text/csv")
            .body(file);
    }

    @PostMapping("/attendance")
    public AttendanceRecord mark(@RequestBody AttendanceRecord a) {
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