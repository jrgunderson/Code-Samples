package com.something.jrgun.elluckphant.model;

import android.os.AsyncTask;
import android.text.TextUtils;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Date;
import java.text.SimpleDateFormat;


/**
 * Checks Official MegaMillions website for any updates to database (on seperate thread)
 * && updates database if necessary
 */

public class Last25 {

    private static FirebaseDatabase mydatabase; // so all db access based on same instance
    private static ArrayList<ArrayList<String>> last25drawings = null; // last 25 winning numbers pulled from website
    private static String allpick5 = null;
    private static String allmega = null;

    // constructor
    public Last25()
    {
        new GetLast25().execute();
    }


    // retrieve last 25 winning numbers from lottery's official website
    private class GetLast25 extends AsyncTask<Void, Void, Void>
    {
        @Override
        protected Void doInBackground(Void... params)
        {
            try {
                Document doc = Jsoup.connect("http://www.megamillions.com/winning-numbers/last-25-drawings").userAgent("mozilla/17.0").get();
                Elements winning_numbers_table = doc.select("tr");

                // save winning lotto picks into 2D list
                last25drawings = new ArrayList<ArrayList<String>>();
                for (Element e : winning_numbers_table)
                {
                    last25drawings.add(new ArrayList<String>(e.getElementsByTag("td").eachText()));
                }

            } catch (IOException e)
            {
                e.printStackTrace();
            }

            // size will be zero if wifi doesn't allow access to megamillions website
            if( last25drawings != null)
            {
                checkLast25();
            }

            return null; // required return statement for AsyncTasks
        }

        @Override
        protected void onPostExecute(Void result) {

        }
    }


    // double check lotto website vs my database
    private void checkLast25()
    {
        mydatabase = FirebaseDatabase.getInstance();
        mydatabase.getReference("lastupdate").addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot)
            {
                SimpleDateFormat formatter = new SimpleDateFormat("M/d/yyyy");
                Date lastupdate = null;
                Date lastdraw = null;

                // date needs try-catch to not throw error
                try {
                    lastupdate = formatter.parse(dataSnapshot.getValue(String.class));
                    lastdraw = formatter.parse(last25drawings.get(1).get(0));
                }
                catch(ParseException e) {
                    e.printStackTrace();
                }
                print("last update: " + lastupdate);
                print("last draw: " + lastdraw);

                // if db needs updating
                if( lastupdate.before(lastdraw) )
                {
                    ArrayList<String> newpick5 = new ArrayList<>();
                    ArrayList<String> newmega = new ArrayList<>();
                    ArrayList<String> thisdraw;

                    // iterate through winning draws in ascending order
                    for (int i=last25drawings.size()-1; i>0; --i) //intentionally avoid header
                    {
                        Date thisdate = null;
                        thisdraw = last25drawings.get(i);

                        try {
                            thisdate = formatter.parse(thisdraw.get(0));
                        }
                        catch(ParseException e) {
                            e.printStackTrace();
                        }

                        // ignore all draws before lastupdate
                        if( thisdate.after(lastupdate) )
                        {
                            print("needs to be added: " + thisdraw);

                            // save them to the front of their respective arrays
                            newpick5.addAll(0, thisdraw.subList(1,6) );
                            newmega.add(0, thisdraw.get(6) );
                        }
                    }

                    // okay now update database
                    updateDatabase( TextUtils.join(" ", newpick5), TextUtils.join(" ", newmega), formatter.format(lastdraw) );

                }
                // else do nothing
                else{
                    print("Database up to date!");
                }

            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });
    }


    // updates lotto numbers in my database
    private void updateDatabase(final String newpick5, final String newmega, final String lastdraw)
    {
        // first retrieve SINGLE REFERENCE data (NOT an open thread)
        mydatabase.getReference("winning5").addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot)
            {
//                String[] split = dataSnapshot.getValue(String.class).split("\\s+");
//                allpick5 = newpick5 + " " + TextUtils.join(" ", split);

                allpick5 = newpick5 + " " + dataSnapshot.getValue(String.class);
                mydatabase.getReference().child("winning5").setValue(allpick5);

                print("new pick 5 balls added: " + newpick5);
            }
            @Override
            public void onCancelled(DatabaseError databaseError) {
            }
        });

        mydatabase.getReference("winningmega").addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot)
            {
                allmega = newmega + " " + dataSnapshot.getValue(String.class);

                mydatabase.getReference().child("winningmega").setValue(allmega);
                mydatabase.getReference().child("lastupdate").setValue(lastdraw);

                print("new mega balls added: " + newmega);
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

    // generic 2D printing of arraylist objects for troubleshooting
    public static <T> void print2D( ArrayList<ArrayList<T>> al)
    {
        for( ArrayList<T> l : al )
        {
            System.out.println(l);
        }
    }
}
