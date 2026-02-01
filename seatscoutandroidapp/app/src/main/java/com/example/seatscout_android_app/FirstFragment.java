package com.example.seatscout_android_app;

import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import okhttp3.*;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import com.example.seatscout_android_app.databinding.FragmentFirstBinding;

import java.util.HashMap;
import java.util.Map;

public class FirstFragment extends Fragment {

    private FragmentFirstBinding binding;
    private static final String BASE_URL = "https://unformalistic-unlikely-glady.ngrok-free.dev/";
    private ApiService apiService;
    private String selectId = "A1";
    private Map<String, String> boothStatuses = new HashMap<>();    //AI

    @Override
    public View onCreateView(
        @NonNull LayoutInflater inflater, ViewGroup container,
        Bundle savedInstanceState){
        //---------------AI-Starts-Here-------------------
        Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

        apiService = retrofit.create(ApiService.class);
        //---------------AI-Ends-Here-------------------

        binding = FragmentFirstBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    private void reserveBooth(String spaceId) {
        Call<ReservationResponse> call = apiService.reserveSpace(spaceId);

        call.enqueue(new Callback<ReservationResponse>() {
            @Override
            public void onResponse(@NonNull Call<ReservationResponse> call, @NonNull Response<ReservationResponse> response) {
                if (response.isSuccessful()) { //AI
                    assert response.body() != null;
                    Toast.makeText(getContext(),
                            response.body().message,
                            Toast.LENGTH_SHORT).show();
                    updateBoothStatus();
                }
            }

            @Override
            public void onFailure(@NonNull Call<ReservationResponse> call, @NonNull Throwable t) {
                Toast.makeText(getContext(),
                        "Connection failed: " + t.getMessage(),
                        Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void updateBoothStatus() {
        //-------------------AI-Starts-Here-------------------
        Call<SpacesResponse> call = apiService.getAllSpaces();

        call.enqueue(new Callback<SpacesResponse>() {
            @Override
            public void onResponse(@NonNull Call<SpacesResponse> call, @NonNull Response<SpacesResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    SpacesResponse spaces = response.body();

        //-----------------AI-Ends-Here-----------------------
                    SpacesResponse.Space boothA1 = spaces.get("A1");
                    SpacesResponse.Space boothA2 = spaces.get("A2");
                    SpacesResponse.Space boothA3 = spaces.get("A3");
                    SpacesResponse.Space boothA4 = spaces.get("A4");
                    SpacesResponse.Space boothA5 = spaces.get("A5");
                    SpacesResponse.Space boothA6 = spaces.get("A6");
                    SpacesResponse.Space boothA7 = spaces.get("A7");
                    SpacesResponse.Space boothA8 = spaces.get("A8");
                    SpacesResponse.Space boothA9 = spaces.get("A9");
                    SpacesResponse.Space boothA10 = spaces.get("A10");

                    if (boothA1 != null) updateBoothUI("booth1", boothA1);
                    if (boothA2 != null) updateBoothUI("booth2", boothA2);
                    if (boothA3 != null) updateBoothUI("booth3", boothA3);
                    if (boothA4 != null) updateBoothUI("booth4", boothA4);
                    if (boothA5 != null) updateBoothUI("booth5", boothA5);
                    if (boothA6 != null) updateBoothUI("booth6", boothA6);
                    if (boothA7 != null) updateBoothUI("booth7", boothA7);
                    if (boothA8 != null) updateBoothUI("booth8", boothA8);
                    if (boothA9 != null) updateBoothUI("booth9", boothA9);
                    if (boothA10 != null) updateBoothUI("booth10", boothA10);

                }
            }

            @Override
            public void onFailure(@NonNull Call<SpacesResponse> call, @NonNull Throwable t) {
                Log.e("API", "Failed to get booth status", t);
                Toast.makeText(getContext(), "Failed to connect to server", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void updateBoothUI(String boothViewId, SpacesResponse.Space booth) {

        int cardId = getResources().getIdentifier(boothViewId, "id", getActivity().getPackageName());  //AI
        assert getView() != null;
        CardView card = getView().findViewById(cardId);


        int textId = getResources().getIdentifier(boothViewId + "Text", "id", getActivity().getPackageName());  //AI
        TextView text = getView().findViewById(textId);

        String status = booth.status != null ? booth.status : "available";  //AI
        String spaceId = getSpaceIdFromViewId(boothViewId);
        boothStatuses.put(spaceId, status);


        // Update color and text based on status
        if ("occupied".equals(status)) {
            card.setCardBackgroundColor(Color.parseColor("#F44336")); // Red
            text.setText("Booth " + boothViewId.toUpperCase() + "\nOccupied\n(" + booth.person_count + "/4)");
            text.setTextColor(Color.WHITE);
        } else if ("reserved".equals(status)) {
            card.setCardBackgroundColor(Color.parseColor("#FFC107")); // Yellow
            text.setText("Booth " + boothViewId.toUpperCase() + "\nReserved");
            text.setTextColor(Color.BLACK);
        } else {
            card.setCardBackgroundColor(Color.parseColor("#4CAF50")); // Green
            text.setText("Booth " + boothViewId.toUpperCase() + "\nAvailable");
            text.setTextColor(Color.WHITE);
        }
    }

    //-------------------AI-Starts-Here-----------
    private String getSpaceIdFromViewId(String boothViewId) {
        // "booth1" -> "A1", "booth2" -> "A2", etc.
        switch(boothViewId) {
            case "booth1": return "A1";
            case "booth2": return "A2";
            case "booth3": return "A3";
            case "booth4": return "A4";
            case "booth5": return "A5";
            case "booth6": return "A6";
            case "booth7": return "A7";
            case "booth8": return "A8";
            case "booth9": return "A9";
            case "booth10": return "A10";
            default: return "A1";
        }
    }
    //-------------------AI-Ends-Here-----------------

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        binding.booth1.setOnClickListener(v ->
                selectId = "A1");
        binding.booth2.setOnClickListener(v ->
                selectId = "A2");
        binding.booth3.setOnClickListener(v ->
                selectId = "A3");
        binding.booth4.setOnClickListener(v ->
                selectId = "A4");
        binding.booth5.setOnClickListener(v ->
                selectId = "A5");
        binding.booth6.setOnClickListener(v ->
                selectId = "A6");
        binding.booth7.setOnClickListener(v ->
                selectId = "A7");
        binding.booth8.setOnClickListener(v ->
                selectId = "A8");
        binding.booth9.setOnClickListener(v ->
                selectId = "A9");
        binding.booth10.setOnClickListener(v ->
                selectId = "A10");
        binding.buttonFirst.setOnClickListener(v -> {
            // Check if booth is available
            String status = boothStatuses.get(selectId);
            if ("reserved".equals(status)) {
                Toast.makeText(getContext(), "This booth is already reserved", Toast.LENGTH_SHORT).show();
                return;
            }
            if ("occupied".equals(status)) {
                Toast.makeText(getContext(), "This booth is occupied", Toast.LENGTH_SHORT).show();
                return;
            }
            reserveBooth(selectId);
        });

        //-------------AI-Starts-Here-------------------
        // Initial status update
        updateBoothStatus();

        // Periodic updates every 2 seconds
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                updateBoothStatus();
                handler.postDelayed(this, 2000);  // Update every 2 seconds
            }
        }, 2000);
        //-------------AI-Ends-Here-------------------
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}