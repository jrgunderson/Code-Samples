package com.something.jrgun.elluckphant.controller;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;

import com.something.jrgun.elluckphant.R;
import com.something.jrgun.elluckphant.model.CalculateStats;
import com.something.jrgun.elluckphant.model.Last25;

public class MainActivity extends AppCompatActivity {

    // check for updates in background
    Last25 l25 = new Last25();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.activity_start);

        // Touch anywhere to continue
        LinearLayout startScreen = (LinearLayout)findViewById(R.id.startScreen);
        startScreen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {

                // generate statistics && updates singleton variables
                CalculateStats cs = new CalculateStats();

                startActivity( new Intent(MainActivity.this, MainMenuActivity.class) );
            }
        });


    }
}
