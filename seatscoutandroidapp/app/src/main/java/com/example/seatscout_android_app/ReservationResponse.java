package com.example.seatscout_android_app;

public class ReservationResponse {
    public String message;
    public String error;
    public double reserved_until;
    public Space space;

    public static class Space {
        public int floor;
        public String status;
        public int person_count;
    }
}