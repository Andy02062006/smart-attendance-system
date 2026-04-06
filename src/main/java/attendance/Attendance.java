package attendance;

public class Attendance {

    private String name;
    private String time;

    public Attendance(String name, String time) {
        this.name = name;
        this.time = time;
    }

    public String getName() {
        return name;
    }

    public String getTime() {
        return time;
    }
}