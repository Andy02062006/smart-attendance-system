package attendance;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
public class AttendanceController {

    @GetMapping("/attendance")
    public List<Attendance> getAttendance() {
        return CSVService.getAttendance();
    }
}