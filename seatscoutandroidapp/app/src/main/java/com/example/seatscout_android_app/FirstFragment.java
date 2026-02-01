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

public class FirstFragment extends Fragment {

    private FragmentFirstBinding binding;
    private static final String BASE_URL = "http://192.168.2.30:5000/";
    private ApiService apiService;

    @Override
    public View onCreateView(
        @NonNull LayoutInflater inflater, ViewGroup container,
        Bundle savedInstanceState){

        Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

        apiService = retrofit.create(ApiService.class);

        binding = FragmentFirstBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    private void reserveBooth(String spaceId) {
        Call<ReservationResponse> call = apiService.reserveSpace(spaceId);

        call.enqueue(new Callback<ReservationResponse>() {
            @Override
            public void onResponse(@NonNull Call<ReservationResponse> call, @NonNull Response<ReservationResponse> response) {
                if (response.isSuccessful()) {
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
        Call<SpacesResponse> call = apiService.getAllSpaces();

        call.enqueue(new Callback<SpacesResponse>() {
            @Override
            public void onResponse(@NonNull Call<SpacesResponse> call, @NonNull Response<SpacesResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    SpacesResponse spaces = response.body();

                    SpacesResponse.Space boothA1 = spaces.get("A1");
                    SpacesResponse.Space boothA2 = spaces.get("A2");
                    SpacesResponse.Space boothA3 = spaces.get("A3");

                    if (boothA1 != null) updateBoothUI("booth1", boothA1);
                    if (boothA2 != null) updateBoothUI("booth2", boothA2);
                    if (boothA3 != null) updateBoothUI("booth3", boothA3);
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
        // Get the CardView
        int cardId = getResources().getIdentifier(boothViewId, "id", getActivity().getPackageName());
        assert getView() != null;
        CardView card = getView().findViewById(cardId);

        // Get the TextView inside the card
        int textId = getResources().getIdentifier(boothViewId + "Text", "id", getActivity().getPackageName());
        TextView text = getView().findViewById(textId);

        // Update color and text based on status
        if (booth.status.equals("occupied")) {
            card.setCardBackgroundColor(Color.parseColor("#F44336")); // Red
            text.setText("Booth " + boothViewId.toUpperCase() + "\nOccupied\n(" + booth.person_count + "/4)");
            text.setTextColor(Color.WHITE);
        } else if (booth.status.equals("reserved")) {
            card.setCardBackgroundColor(Color.parseColor("#FFC107")); // Yellow
            text.setText("Booth " + boothViewId.toUpperCase() + "\nReserved");
            text.setTextColor(Color.BLACK);
        } else {
            card.setCardBackgroundColor(Color.parseColor("#4CAF50")); // Green
            text.setText("Booth " + boothViewId.toUpperCase() + "\nAvailable");
            text.setTextColor(Color.WHITE);
        }
    }


    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        binding.buttonFirst.setOnClickListener(v ->
                reserveBooth("A1")
        );

        //-------------AI-Starts-Here-------------------
        // Initial status update
        updateBoothStatus();

        // Periodic updates every 5 seconds
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                updateBoothStatus();
                handler.postDelayed(this, 5000);  // Update every 5 seconds
            }
        }, 5000);
        //-------------AI-Ends-Here-------------------
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}