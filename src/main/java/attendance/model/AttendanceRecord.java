package attendance.model;

/**
 * SRS & Class Diagram aligned AttendanceRecord
 */
public class AttendanceRecord {
    public String name;
    public String time;
    public String status; // Present/Absent
    public String engagement; // SRS: Engagement Monitoring

    public AttendanceRecord() {}

    public AttendanceRecord(String name, String time, String status, String engagement) {
        this.name = name;
        this.time = time;
        this.status = status;
        this.engagement = engagement;
    }
}
