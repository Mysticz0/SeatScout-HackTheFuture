package com.example.seatscout_android_app;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface ApiService {

    @GET("check-all-spaces")
    Call<SpacesResponse> getAllSpaces();

    @POST("reserve-space/{space_id}")
    Call<ReservationResponse> reserveSpace(@Path("space_id") String spaceId);
}
