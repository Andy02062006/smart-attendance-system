package attendance.model;

public class Attendance {
    public String name;
    public String time;
    public String engagement; // SRS: Engagement Monitoring

    public Attendance() {}

    public Attendance(String name, String time, String engagement) {
        this.name = name;
        this.time = time;
        this.engagement = engagement;
    }
}