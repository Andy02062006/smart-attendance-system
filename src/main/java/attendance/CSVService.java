package attendance;

import java.io.*;
import java.util.*;

public class CSVService {

    public static List<Attendance> getAttendance() {
        List<Attendance> list = new ArrayList<>();

        try {
            BufferedReader br = new BufferedReader(new FileReader("/Users/andreaj.b/Desktop/chatbot/attendance/attendance.csv"));
            String line;

            br.readLine(); // skip header

            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                list.add(new Attendance(data[0], data[1]));
            }

            br.close();

        } catch (Exception e) {
            System.out.println("Error reading CSV");
        }

        return list;
    }
}