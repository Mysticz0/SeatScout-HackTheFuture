package com.example.seatscout_android_app;

import com.google.gson.annotations.SerializedName;

import java.util.HashMap;

public class SpacesResponse extends HashMap<String, SpacesResponse.Space> {

    public static class Space {
        public int floor;
        public String status;
        public int person_count;
        public Double reserved_until;
        public Double reservation_time;
    }
}