package attendance.service;

import attendance.model.AttendanceRecord;
import java.io.*;
import java.util.*;

public class CSVService {
    static String FILE = "attendance.csv";

    public static List<AttendanceRecord> getAttendance() {
        List<AttendanceRecord> list = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(FILE))) {
            br.readLine(); 
            String l;
            while ((l = br.readLine()) != null) {
                String[] d = l.split(",");
                if (d.length >= 4) list.add(new AttendanceRecord(d[0], d[1], d[2], d[3]));
            }
        } catch (Exception e) {}
        return list;
    }

    public static void saveAttendance(AttendanceRecord a) {
        String today = java.time.LocalDate.now().toString();
        for (AttendanceRecord e : getAttendance()) 
            if (e.name.equalsIgnoreCase(a.name) && e.time.startsWith(today)) return;

        try (PrintWriter pw = new PrintWriter(new FileWriter(FILE, true))) {
            pw.println(a.name + "," + a.time + "," + a.status + "," + a.engagement);
        } catch (Exception e) {}
    }

    public static void resetAttendance() {
        try (PrintWriter pw = new PrintWriter(new FileWriter(FILE))) {
            pw.println("name,time,status,engagement"); 
        } catch (Exception e) {}
    }

    public static Map<String, Object> getStats() {
        List<AttendanceRecord> records = getAttendance();
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalAttendance", records.size());
        
        long active = records.stream().filter(r -> "Active".equalsIgnoreCase(r.engagement)).count();
        long drowsy = records.stream().filter(r -> "Drowsy".equalsIgnoreCase(r.engagement)).count();
        long distracted = records.stream().filter(r -> "Distracted".equalsIgnoreCase(r.engagement)).count();
        
        stats.put("active", active);
        stats.put("drowsy", drowsy);
        stats.put("distracted", distracted);
        return stats;
    }
}