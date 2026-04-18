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
}