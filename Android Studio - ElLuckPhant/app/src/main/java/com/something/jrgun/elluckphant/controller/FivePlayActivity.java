package com.something.jrgun.elluckphant.controller;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.something.jrgun.elluckphant.R;
import com.something.jrgun.elluckphant.model.GenerateNumbers;

import java.util.ArrayList;
import java.util.Arrays;


/**
 * Generates 5 sets of numbers from lotto stats
 * (There is no repeating numbers in those 5 sets)
 */

public class FivePlayActivity extends AppCompatActivity
{
    private ArrayList<ArrayList<TextView>> balls;
    GenerateNumbers generateNumbers = new GenerateNumbers( 1 ); // initialize


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.activity_5plays);

        // fill TextView Arrays
        fillBalls();

        // to main
        Button toMainFrom5Plays = (Button)findViewById(R.id.toMainFrom5Plays);
        toMainFrom5Plays.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                startActivity( new Intent(FivePlayActivity.this, MainMenuActivity.class) );
            }
        });

        // to 1 Play
        Button to1PlayFrom5Plays = (Button)findViewById(R.id.to1PlayFrom5Plays);
        to1PlayFrom5Plays.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                startActivity( new Intent(FivePlayActivity.this, OnePlayActivity.class) );
            }
        });


        // generate 5 sets of lotto numbers
        Button generate = (Button) findViewById(R.id.generate5);
        generate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                // generate lotto numbers
                ArrayList<ArrayList<Integer>> play5 = generateNumbers.statisticalPlay5();

                // if loading fails -> just randomly generate numbers
                if( play5 == null )
                {

                    for(int i=0; i<5; ++i)
                    {
                        // generate lotto numbers
                        ArrayList<Integer> lottoNumbers = generateNumbers.generateRandom();
                        System.out.println(lottoNumbers);

                        // update ball TextViews with lotto numbers
                        for(int j=0; j<6; ++j)
                        {
                            balls.get(i).get(j).setText( Integer.toString(lottoNumbers.get(j)) );
                        }
                    }
                }
                // else we can generate numbers based on statistics!!
                else
                {
                    System.out.println("Picks Generated");
                    for(int i=0; i<5; ++i)
                    {
                        System.out.println(play5.get(i));

                        // update ball TextViews with lotto numbers
                        for(int j=0; j<6; ++j)
                        {
                            balls.get(i).get(j).setText( Integer.toString(play5.get(i).get(j)) );
                        }
                    }
                }

            }

        });

    } // end onCreate


    // add ball TextViews to an array
    void fillBalls()
    {
        balls = new ArrayList<ArrayList<TextView>>();
        balls.add(new ArrayList<TextView>(Arrays.asList(
            (TextView) findViewById(R.id.a1),
            (TextView) findViewById(R.id.a2),
            (TextView) findViewById(R.id.a3),
            (TextView) findViewById(R.id.a4),
            (TextView) findViewById(R.id.a5),
            (TextView) findViewById(R.id.a6) )));
        balls.add(new ArrayList<TextView>(Arrays.asList(
            (TextView) findViewById(R.id.b1),
            (TextView) findViewById(R.id.b2),
            (TextView) findViewById(R.id.b3),
            (TextView) findViewById(R.id.b4),
            (TextView) findViewById(R.id.b5),
            (TextView) findViewById(R.id.b6) )));
        balls.add(new ArrayList<TextView>(Arrays.asList(
            (TextView) findViewById(R.id.c1),
            (TextView) findViewById(R.id.c2),
            (TextView) findViewById(R.id.c3),
            (TextView) findViewById(R.id.c4),
            (TextView) findViewById(R.id.c5),
            (TextView) findViewById(R.id.c6) )));
        balls.add(new ArrayList<TextView>(Arrays.asList(
            (TextView) findViewById(R.id.d1),
            (TextView) findViewById(R.id.d2),
            (TextView) findViewById(R.id.d3),
            (TextView) findViewById(R.id.d4),
            (TextView) findViewById(R.id.d5),
            (TextView) findViewById(R.id.d6) )));
        balls.add(new ArrayList<TextView>(Arrays.asList(
            (TextView) findViewById(R.id.e1),
            (TextView) findViewById(R.id.e2),
            (TextView) findViewById(R.id.e3),
            (TextView) findViewById(R.id.e4),
            (TextView) findViewById(R.id.e5),
            (TextView) findViewById(R.id.e6) )));
    }


} // end class
