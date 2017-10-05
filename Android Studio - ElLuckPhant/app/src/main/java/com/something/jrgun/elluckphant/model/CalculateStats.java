package com.something.jrgun.elluckphant.model;

import android.util.Log;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.something.jrgun.elluckphant.HoldStats;
import java.util.HashMap;

/**
 * This class generates statistics on each number pulled from a lottery drawing
 *
 * It fills the singleton 'global variable' so the statistics only need to be generated once
 *
 * This is an open thread to ensure statistics are always up to date
 *
 * My Firebase database contains lists of all previously pulled lottery numbers
 * (note: only winning numbers past 10/25/2013,
 *  since that's when the format changed to numbers (1 - 75) for Pick 5  &&  (1 - 15) for Powerball )
 */

public class CalculateStats
{
    private static FirebaseDatabase mydatabase; // so stats based on same instance
    private static HashMap<Integer, Integer> pick5stats; // keeps track of how many times
    private static HashMap<Integer, Integer> megaBstats; // each ball has been picked
    private double numOfLottos;

    // default constructor
    public CalculateStats()
    {
        mydatabase = FirebaseDatabase.getInstance();
        fill5stats();
        fillMegaStats(); // will finish first since less complicated code
    }


    // fill stats for pick 5 from file
    private void fill5stats()
    {
        // opens thread
        mydatabase.getReference("winning5").addValueEventListener(new ValueEventListener() {

            @Override
            public void onDataChange(DataSnapshot dataSnapshot)
            {
                pick5stats = new HashMap<>();

                for (int i = 1; i <= 75; ++i) {
                    pick5stats.put(i, 0); // initialize with zeros
                }

                double checkNumOfLottos = 0;
                String[] split = dataSnapshot.getValue(String.class).split("\\s+");

                for(String s : split)
                {
                    int num = Integer.parseInt(s);
                    pick5stats.put(num, pick5stats.get(num) + 1); // increment stat count;

                    ++checkNumOfLottos;
                }

                HoldStats.getInstance().setPick5stats(pick5stats);
                checkNumOfLottos /= 5;

                print("pick 5 stats: " + pick5stats);
                print("Num of Lottos from Pick5: " + checkNumOfLottos);

                // if for some reason fill5 is called before fillMega
                if(numOfLottos==0)
                {
                    numOfLottos = checkNumOfLottos;
                    HoldStats.getInstance().setNumOfLottos(numOfLottos);
                }

                // Quality Assurance
                if(checkNumOfLottos != numOfLottos)
                {
                    Log.e("WARNING", "NUM OF LOTTOS DO NOT MATCH");
                    System.out.println(numOfLottos + " " + checkNumOfLottos);
                }

            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });
    }


    // fill stats for mega ball from file
    private void fillMegaStats()
    {
        // opens another thread
        mydatabase.getReference("winningmega").addValueEventListener(new ValueEventListener() {

            @Override
            public void onDataChange(DataSnapshot dataSnapshot)
            {
                if(numOfLottos != 0){ numOfLottos = 0;}

                megaBstats = new HashMap<>();

                for( int i=1; i<=15; ++i )
                {
                    megaBstats.put( i, 0 ); // initialize with zeros
                }

                String[] split = dataSnapshot.getValue(String.class).split("\\s+");

                for(String s : split)
                {
                    int num = Integer.parseInt(s);
                    megaBstats.put(num, megaBstats.get(num) + 1); // increment stat count;

                    ++numOfLottos;
                }

                HoldStats.getInstance().setMegaBstats(megaBstats);
                HoldStats.getInstance().setNumOfLottos(numOfLottos);

                print("megaball stats: " + megaBstats);
                print("Num of Lottos from Mega: " + numOfLottos);
                print("Expected number of pulls: " + numOfLottos/15.0);
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });
    }


    // to reduce the typing involved in print statements
    public static <T> void print( T t)
    {
        System.out.println(t);
    }


} // end class
