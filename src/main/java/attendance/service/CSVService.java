package attendance.service;

import attendance.model.AttendanceRecord;
import java.io.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class CSVService {
    static String FILE = "attendance.csv";
    static List<attendance.model.EngagementAlert> alerts = new ArrayList<>();
    static Map<String, AttendanceRecord> detections = new ConcurrentHashMap<>();

    public static List<AttendanceRecord> getDetections() {
        return new ArrayList<>(detections.values());
    }

    public static void updateDetection(AttendanceRecord r) {
        detections.put(r.name, r);
    }

    public static List<attendance.model.EngagementAlert> getAlerts() {
        return new ArrayList<>(alerts);
    }

    public static void addAlert(attendance.model.EngagementAlert alert) {
        alerts.add(0, alert);
        if (alerts.size() > 20) alerts.remove(alerts.size() - 1);
    }

    public static void clearAlerts() {
        alerts.clear();
    }

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
        long drowsy = records.stream().filter(r -> r.engagement != null && r.engagement.contains("Drowsy")).count();
        long distracted = records.stream().filter(r -> "Distracted".equalsIgnoreCase(r.engagement)).count();
        
        stats.put("active", active);
        stats.put("drowsy", drowsy);
        stats.put("distracted", distracted);
        return stats;
    }

    public static List<Map<String, Object>> getAbsenceStats() {
        List<String> allStudents = Arrays.asList("Andrea", "Aishwarya");
        List<AttendanceRecord> records = getAttendance();
        List<Map<String, Object>> stats = new ArrayList<>();
        
        Map<String, Set<String>> presenceMap = new HashMap<>();
        Set<String> allDates = new HashSet<>();
        
        for (AttendanceRecord r : records) {
            String date = r.time.split(" ")[0];
            allDates.add(date);
            presenceMap.putIfAbsent(r.name, new HashSet<>());
            presenceMap.get(r.name).add(date);
        }
        
        int totalDays = allDates.size();
        if (totalDays == 0) totalDays = 1;

        for (String student : allStudents) {
            Set<String> presentDates = presenceMap.getOrDefault(student, new HashSet<>());
            int absentCount = totalDays - presentDates.size();
            
            Map<String, Object> s = new HashMap<>();
            s.put("name", student);
            s.put("absentCount", absentCount);
            s.put("attendanceRate", (int)((presentDates.size() * 100.0) / totalDays));
            
            List<String> absentDates = new ArrayList<>(allDates);
            absentDates.removeAll(presentDates);
            Collections.sort(absentDates, Collections.reverseOrder());
            s.put("lastAbsent", absentDates.isEmpty() ? "Never" : absentDates.get(0));
            stats.add(s);
        }
        
        stats.sort((a, b) -> (Integer)b.get("absentCount") - (Integer)a.get("absentCount"));
        return stats;
    }
}