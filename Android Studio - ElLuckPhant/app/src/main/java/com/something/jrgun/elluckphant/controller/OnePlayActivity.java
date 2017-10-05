package com.something.jrgun.elluckphant.controller;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.something.jrgun.elluckphant.R;
import com.something.jrgun.elluckphant.model.GenerateNumbers;

import java.util.ArrayList;

/**
 * This Activity generates the numbers randomly
 * So user can compare the random numbers to the statistical generated numbers
 */

public class OnePlayActivity extends AppCompatActivity {

    private ArrayList<TextView> balls;
    private ArrayList<ImageView> pick5ticket;
    private ArrayList<ImageView> megaticket;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.activity_1play);

        // fill TextView Arrays
        fillBalls();
        fillTicket();

        // to main
        Button toMainFrom1Play = (Button)findViewById(R.id.toMainFrom1Play);
        toMainFrom1Play.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                startActivity( new Intent(OnePlayActivity.this, MainMenuActivity.class) );
            }
        });

        // to 5 Plays
        Button to5PlaysFrom1Play = (Button)findViewById(R.id.to5PlaysFrom1Play);
        to5PlaysFrom1Play.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                startActivity( new Intent(OnePlayActivity.this, FivePlayActivity.class) );
            }
        });

        // generate 1 set of lotto numbers
        Button generate = (Button) findViewById(R.id.generate1);
        generate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {

                // reset visibility on ticket
                for(int i=0; i<pick5ticket.size(); ++i)
                {
                    ImageView iv = pick5ticket.get(i);
                    if( iv.getVisibility() == View.VISIBLE )
                    {
                        iv.setVisibility(View.INVISIBLE);
                    }
                }
                for(int i=0; i<megaticket.size(); ++i)
                {
                    ImageView iv = megaticket.get(i);
                    if( iv.getVisibility() == View.VISIBLE )
                    {
                        iv.setVisibility(View.INVISIBLE);
                    }
                }


                // generate lotto numbers
                ArrayList<Integer> lottoNumbers = new GenerateNumbers().getNums();
                System.out.println(lottoNumbers);


                // update ball TextViews with lotto numbers
                for(int i=0; i<5; ++i)
                {
                    int number = lottoNumbers.get(i);
                    balls.get(i).setText( Integer.toString(number) );
                    pick5ticket.get(number-1).setVisibility(View.VISIBLE); // -1 because array 0 indexed
                }
                int number = lottoNumbers.get(5);
                balls.get(5).setText( Integer.toString(number) );
                megaticket.get(number-1).setVisibility(View.VISIBLE); // -1 because array 0 indexed

            }
        });

    } // end onCreate

    // add ball TextViews to an array
    void fillBalls()
    {
        balls = new ArrayList<>();
        balls.add( (TextView) findViewById(R.id.ball1) );
        balls.add( (TextView) findViewById(R.id.ball2) );
        balls.add( (TextView) findViewById(R.id.ball3) );
        balls.add( (TextView) findViewById(R.id.ball4) );
        balls.add( (TextView) findViewById(R.id.ball5) );
        balls.add( (TextView) findViewById(R.id.megaball) );
    }

    // add lotto ticket TextViews to an array
    void fillTicket()
    {
        pick5ticket = new ArrayList<>();
        pick5ticket.add( (ImageView) findViewById(R.id.t1) );
        pick5ticket.add( (ImageView) findViewById(R.id.t2) );
        pick5ticket.add( (ImageView) findViewById(R.id.t3) );
        pick5ticket.add( (ImageView) findViewById(R.id.t4) );
        pick5ticket.add( (ImageView) findViewById(R.id.t5) );
        pick5ticket.add( (ImageView) findViewById(R.id.t6) );
        pick5ticket.add( (ImageView) findViewById(R.id.t7) );
        pick5ticket.add( (ImageView) findViewById(R.id.t8) );
        pick5ticket.add( (ImageView) findViewById(R.id.t9) );
        pick5ticket.add( (ImageView) findViewById(R.id.t10) );
        pick5ticket.add( (ImageView) findViewById(R.id.t11) );
        pick5ticket.add( (ImageView) findViewById(R.id.t12) );
        pick5ticket.add( (ImageView) findViewById(R.id.t13) );
        pick5ticket.add( (ImageView) findViewById(R.id.t14) );
        pick5ticket.add( (ImageView) findViewById(R.id.t15) );
        pick5ticket.add( (ImageView) findViewById(R.id.t16) );
        pick5ticket.add( (ImageView) findViewById(R.id.t17) );
        pick5ticket.add( (ImageView) findViewById(R.id.t18) );
        pick5ticket.add( (ImageView) findViewById(R.id.t19) );
        pick5ticket.add( (ImageView) findViewById(R.id.t20) );
        pick5ticket.add( (ImageView) findViewById(R.id.t21) );
        pick5ticket.add( (ImageView) findViewById(R.id.t22) );
        pick5ticket.add( (ImageView) findViewById(R.id.t23) );
        pick5ticket.add( (ImageView) findViewById(R.id.t24) );
        pick5ticket.add( (ImageView) findViewById(R.id.t25) );
        pick5ticket.add( (ImageView) findViewById(R.id.t26) );
        pick5ticket.add( (ImageView) findViewById(R.id.t27) );
        pick5ticket.add( (ImageView) findViewById(R.id.t28) );
        pick5ticket.add( (ImageView) findViewById(R.id.t29) );
        pick5ticket.add( (ImageView) findViewById(R.id.t30) );
        pick5ticket.add( (ImageView) findViewById(R.id.t31) );
        pick5ticket.add( (ImageView) findViewById(R.id.t32) );
        pick5ticket.add( (ImageView) findViewById(R.id.t33) );
        pick5ticket.add( (ImageView) findViewById(R.id.t34) );
        pick5ticket.add( (ImageView) findViewById(R.id.t35) );
        pick5ticket.add( (ImageView) findViewById(R.id.t36) );
        pick5ticket.add( (ImageView) findViewById(R.id.t37) );
        pick5ticket.add( (ImageView) findViewById(R.id.t38) );
        pick5ticket.add( (ImageView) findViewById(R.id.t39) );
        pick5ticket.add( (ImageView) findViewById(R.id.t40) );
        pick5ticket.add( (ImageView) findViewById(R.id.t41) );
        pick5ticket.add( (ImageView) findViewById(R.id.t42) );
        pick5ticket.add( (ImageView) findViewById(R.id.t43) );
        pick5ticket.add( (ImageView) findViewById(R.id.t44) );
        pick5ticket.add( (ImageView) findViewById(R.id.t45) );
        pick5ticket.add( (ImageView) findViewById(R.id.t46) );
        pick5ticket.add( (ImageView) findViewById(R.id.t47) );
        pick5ticket.add( (ImageView) findViewById(R.id.t48) );
        pick5ticket.add( (ImageView) findViewById(R.id.t49) );
        pick5ticket.add( (ImageView) findViewById(R.id.t50) );
        pick5ticket.add( (ImageView) findViewById(R.id.t51) );
        pick5ticket.add( (ImageView) findViewById(R.id.t52) );
        pick5ticket.add( (ImageView) findViewById(R.id.t53) );
        pick5ticket.add( (ImageView) findViewById(R.id.t54) );
        pick5ticket.add( (ImageView) findViewById(R.id.t55) );
        pick5ticket.add( (ImageView) findViewById(R.id.t56) );
        pick5ticket.add( (ImageView) findViewById(R.id.t57) );
        pick5ticket.add( (ImageView) findViewById(R.id.t58) );
        pick5ticket.add( (ImageView) findViewById(R.id.t59) );
        pick5ticket.add( (ImageView) findViewById(R.id.t60) );
        pick5ticket.add( (ImageView) findViewById(R.id.t61) );
        pick5ticket.add( (ImageView) findViewById(R.id.t62) );
        pick5ticket.add( (ImageView) findViewById(R.id.t63) );
        pick5ticket.add( (ImageView) findViewById(R.id.t64) );
        pick5ticket.add( (ImageView) findViewById(R.id.t65) );
        pick5ticket.add( (ImageView) findViewById(R.id.t66) );
        pick5ticket.add( (ImageView) findViewById(R.id.t67) );
        pick5ticket.add( (ImageView) findViewById(R.id.t68) );
        pick5ticket.add( (ImageView) findViewById(R.id.t69) );
        pick5ticket.add( (ImageView) findViewById(R.id.t70) );
        pick5ticket.add( (ImageView) findViewById(R.id.t71) );
        pick5ticket.add( (ImageView) findViewById(R.id.t72) );
        pick5ticket.add( (ImageView) findViewById(R.id.t73) );
        pick5ticket.add( (ImageView) findViewById(R.id.t74) );
        pick5ticket.add( (ImageView) findViewById(R.id.t75) );
        megaticket = new ArrayList<>();
        megaticket.add( (ImageView) findViewById(R.id.m1) );
        megaticket.add( (ImageView) findViewById(R.id.m2) );
        megaticket.add( (ImageView) findViewById(R.id.m3) );
        megaticket.add( (ImageView) findViewById(R.id.m4) );
        megaticket.add( (ImageView) findViewById(R.id.m5) );
        megaticket.add( (ImageView) findViewById(R.id.m6) );
        megaticket.add( (ImageView) findViewById(R.id.m7) );
        megaticket.add( (ImageView) findViewById(R.id.m8) );
        megaticket.add( (ImageView) findViewById(R.id.m9) );
        megaticket.add( (ImageView) findViewById(R.id.m10) );
        megaticket.add( (ImageView) findViewById(R.id.m11) );
        megaticket.add( (ImageView) findViewById(R.id.m12) );
        megaticket.add( (ImageView) findViewById(R.id.m13) );
        megaticket.add( (ImageView) findViewById(R.id.m14) );
        megaticket.add( (ImageView) findViewById(R.id.m15) );
    }


} // end class
