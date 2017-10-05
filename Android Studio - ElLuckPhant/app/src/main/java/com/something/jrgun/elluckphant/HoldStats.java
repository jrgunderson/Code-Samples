package com.something.jrgun.elluckphant;

import java.util.HashMap;

/**
 * Singleton class:
 * Ability to share variables across Activities
 * Only allows one instance of these variables
 *
 * Keeps track of number of times each ball has been picked
 */

public class HoldStats
{
    private static final HoldStats ourInstance = new HoldStats();

    private static HashMap<Integer, Integer> pick5stats = null;
    private static HashMap<Integer, Integer> megaBstats = null;
    private double numOfLottos;

    // retrieves the instance from anywhere
    public static HoldStats getInstance() {
        return ourInstance;
    }

    // private constructor to prevent multiple instances
    private HoldStats() {
    }


    // getters
    public static HashMap<Integer, Integer> getPick5stats() {
        return pick5stats;
    }

    public static HashMap<Integer, Integer> getMegaBstats() {
        return megaBstats;
    }

    public double getNumOfLottos() {
        return numOfLottos;
    }


    // setters
    public static void setPick5stats(HashMap<Integer, Integer> pick5stats) {
        HoldStats.pick5stats = pick5stats;
    }

    public static void setMegaBstats(HashMap<Integer, Integer> megaBstats) {
        HoldStats.megaBstats = megaBstats;
    }

    public void setNumOfLottos(double numOfLottos) {
        this.numOfLottos = numOfLottos;
    }

    // set all variables
    public void setAll(HashMap<Integer, Integer> p5s, HashMap<Integer, Integer> mbs, double nol)
    {
        pick5stats = p5s;
        megaBstats = mbs;
        numOfLottos = nol;
    }


}
