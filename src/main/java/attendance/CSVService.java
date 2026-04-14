package attendance;

import java.io.*;
import java.util.*;

public class CSVService {
    private static final String CSV_FILE = "attendance.csv";

    public static List<Attendance> getAttendance() {
        List<Attendance> list = new ArrayList<>();
        File file = new File(CSV_FILE);
        
        if (!file.exists()) {
            return list;
        }

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            br.readLine(); // skip header

            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                if (data.length >= 2) {
                    list.add(new Attendance(data[0], data[1]));
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return list;
    }

    public static void saveAttendance(Attendance attendance) {
        File file = new File(CSV_FILE);
        boolean exists = file.exists();
        
        try (PrintWriter pw = new PrintWriter(new FileWriter(file, true))) {
            if (!exists) {
                pw.println("Name,Time");
            }
            pw.println(attendance.getName() + "," + attendance.getTime());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}