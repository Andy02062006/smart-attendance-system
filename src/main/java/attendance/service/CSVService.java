package attendance.service;

import attendance.model.Attendance;
import java.io.*;
import java.util.*;

public class CSVService {
    static String FILE = "attendance.csv";

    public static List<Attendance> getAttendance() {
        List<Attendance> list = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(FILE))) {
            br.readLine(); 
            String l;
            while ((l = br.readLine()) != null) {
                String[] d = l.split(",");
                if (d.length >= 3) list.add(new Attendance(d[0], d[1], d[2]));
            }
        } catch (Exception e) {}
        return list;
    }

    public static void saveAttendance(Attendance a) {
        String today = java.time.LocalDate.now().toString();
        for (Attendance e : getAttendance()) 
            if (e.name.equalsIgnoreCase(a.name) && e.time.startsWith(today)) return;

        try (PrintWriter pw = new PrintWriter(new FileWriter(FILE, true))) {
            pw.println(a.name + "," + a.time + "," + a.engagement);
        } catch (Exception e) {}
    }
}