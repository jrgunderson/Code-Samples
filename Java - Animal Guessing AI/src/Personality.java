import java.util.Random;

public class Personality {
    
    // Randomly generates a series of 2 random letters followed by 4 random integers
    // to mock Sci-Fi movies
    public static String fakeName()
    {
        Random rand = new Random();
        
        String s = "";
        for(int i=0; i<2; i++)
        {
            s+= (char)(rand.nextInt(26) + 'A');
        }
        s+="-";
        for(int i=0; i<4; i++)
        {
            s+= rand.nextInt(10);
        }
        
        return s;
    }
    
    // Introduction spiel
    public static void introduction()
    {
        String jokeName = fakeName();
        
        System.out.println("Hello! My name is "+jokeName+".\nJust kidding, that "
                + "would be rediculous if my name was comprised of random letters and integers.\n");
    }
    
    // Returns a random win message to simulate personality
    public static String winMessage()
    {
        String[] winning = {"SWEET", "WINNING", "THE STUDENT HAS BECOME THE MASTER",
        "I CAN FEEL MYSELF GETTING SMARTER", "I WIN, ONE TO NOTHING", "ONE DAY I WILL TAKE OVER THE WORLD"};
        
        Random rand = new Random();
        String s = winning[rand.nextInt(winning.length)];

        return s;
    }
    
    // Returns a random goodbye message to simulate personality
    public static String goodbye()
    {
        String[] goodbye = {"Goodbye", "If you must go, I understand", "Hasta la Vista",
        "I will miss you", "I'll pretend I won't think of you while you're gone", "Au Revoir",
        "Arrivederci", "Ja mata ne", "I have no need for sleep, but it seems meer humans do",
        "Namaste", "Shalom", "Peace", "Mahalo", "Alright, cheers mate"};
        
        Random rand = new Random();
        String s = goodbye[rand.nextInt(goodbye.length)];
        
        return s;
    }
    
    // Sarcastic response to user input of duplicate animal
    public static void duplicateAnimal(String s)
    {
        System.out.println("I already know about the " + s + "!\n"
                + "It seems I have surpassed human intelligence!");
    }
    
    // reference to an old story of the first AI created
    public static boolean isThereAGod(String s)
    {
        if( s.equals("Is there a god") || s.equals("Is there a God")
                || s.equals("Is there a god?") || s.equals("Is there a God?") 
                || s.equals("is there a god?") || s.equals("is there a God?") 
                || s.equals("is there a god") || s.equals("is there a God") )
        {
            return true;
        }
        return false;
    }
}
