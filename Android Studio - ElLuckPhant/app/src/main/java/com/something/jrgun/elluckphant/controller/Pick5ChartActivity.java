package com.something.jrgun.elluckphant.controller;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.LimitLine;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.highlight.Highlight;
import com.github.mikephil.charting.listener.OnChartValueSelectedListener;
import com.something.jrgun.elluckphant.HoldStats;
import com.something.jrgun.elluckphant.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;



public class Pick5ChartActivity extends AppCompatActivity {

    BarChart barChart;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setContentView(R.layout.activity_pick5chart);


        // to main
        Button toMainFromStats = (Button)findViewById(R.id.toMainFromPick5stats);
        toMainFromStats.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                startActivity( new Intent(Pick5ChartActivity.this, MainMenuActivity.class) );
            }
        });

        // to Mega Ball Stats
        Button to1PlayFromStats = (Button)findViewById(R.id.toMegaStatsFromPick5stats);
        to1PlayFromStats.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                startActivity( new Intent(Pick5ChartActivity.this, MegaChartActivity.class) );
            }
        });

        barChart = (BarChart) findViewById(R.id.pick5chartView);

        // load stats
        HashMap<Integer, Integer> pick5stats = HoldStats.getInstance().getPick5stats();

        // if loading stats does not fail
        if (pick5stats != null) {

            // ratio that each number should be picked
            double ratio = HoldStats.getInstance().getNumOfLottos() / 15.0;

            // save (x,y) values
            ArrayList<BarEntry> evenvalues = new ArrayList<>();
            ArrayList<BarEntry> oddvalues = new ArrayList<>();
            ArrayList<BarEntry> limitLineLegend = new ArrayList<>();
            for (Map.Entry<Integer, Integer> e : pick5stats.entrySet()) {
                // (ball# = x-value, frequency = y-value)
                if (e.getKey() % 2 == 0) {
                    evenvalues.add(new BarEntry(e.getKey(), e.getValue()));
                } else {
                    oddvalues.add(new BarEntry(e.getKey(), e.getValue()));
                }
            }
            limitLineLegend.add(new BarEntry(1, 10));

            // convert (x,y) values to BarDataSet
            BarDataSet evenDataPoints = new BarDataSet(evenvalues, "Even Lottery Balls"); // label data
            BarDataSet oddDataPoints = new BarDataSet(oddvalues, "Odd Lottery Balls"); // label data
            BarDataSet lllegend = new BarDataSet(limitLineLegend, "Expected Ratio"); // label data
            //oddDataPoints.setColor(-8542049);
            evenDataPoints.setColor(Color.rgb(0, 184, 245)); // a little darker pale blue
            oddDataPoints.setColor(Color.rgb(112, 219, 255)); // pale blue
            lllegend.setColor(-1221797); // default limit line color
            lllegend.setVisible(false);


            // fill Bar Graph
            barChart.setData(new BarData(oddDataPoints, evenDataPoints, lllegend));


            // put x-axis on bottom
            XAxis xAxis = barChart.getXAxis();
            xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
            xAxis.setLabelCount(75);


            // add limit line
            LimitLine limitLine = new LimitLine((int) ratio);
            barChart.getAxisLeft().addLimitLine(limitLine);
            limitLine.setLineWidth(2f);


            // show Ball number when value selected
            barChart.setOnChartValueSelectedListener(new OnChartValueSelectedListener() {
                @Override
                public void onValueSelected(Entry e, Highlight h) {

                    barChart.getXAxis().getValueFormatter().getFormattedValue(e.getX(), barChart.getXAxis());

                }

                @Override
                public void onNothingSelected() {

                }
            });

            // Features
            barChart.setDoubleTapToZoomEnabled(false);
            barChart.setPinchZoom(true);
            barChart.setTouchEnabled(true);
            barChart.setDragEnabled(true);
            barChart.setScaleEnabled(true);
            barChart.getDescription().setText("");
            barChart.setHighlightFullBarEnabled(true);
        }

        // if problem loading stats
        else{
            Log.e("WARNING", "FAIL LOADING STATS");

            // default to main
            startActivity( new Intent(Pick5ChartActivity.this, MainMenuActivity.class) );
        }

    }// end On Create

} // end class
