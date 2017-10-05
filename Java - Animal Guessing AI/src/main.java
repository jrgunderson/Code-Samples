import java.util.Scanner;

public class main {

    public static void main(String[] args) {
        
        Scanner input = new Scanner(System.in);
        
        // prints header
        animalASCII.printAnimalArt();
        
        Tree<String> animalgame = new Tree<>();
        //animalgame.initialTree();  // resets AI's brain
        animalgame.fromFile();  // loads AI's brain   
        
        
        // AI's introduction
        Personality.introduction();
        
        // actual game
        boolean again = true;
        do{
        
            System.out.println("I want you to picture an animal...\nNow I will ask you a bunch of questions "
                    + "to see if I can figure out what animal you are thinking of.\n");

            // iterates through tree
            Node n = animalgame.getRoot();
            String answer = "";
            while(animalgame.hasChildren(n))  // will iterate until no more leaves in branch
            {
                // will assume that you wont mess up
                boolean notValid = true;
                do{
                    // prints out info on current node
                    System.out.println(n.getData());
                    
                    try{
                        // user input
                        answer = input.nextLine();
                        
                        // if user asks AI "is there a god"
                        if(Personality.isThereAGod(answer))
                        {
                            System.out.println("\nTHERE IS NOW!\n");
                        }
                        // if user enters yes or no
                        else if( answer.charAt(0)=='y' || answer.charAt(0)=='Y'
                                || answer.charAt(0)=='n' || answer.charAt(0)=='N')
                        {
                            notValid = false; // then it is valid input and can continue
                        }
                        else{
                            System.out.println("\nThat is not an answer to a yes or no question!\n");
                        }
                    }
                    catch(Exception e)
                    {
                        input.nextLine();
                    }
                }while(notValid); // will continue to ask for valid input until valid input received

                // traverse through tree
                if((answer.charAt(0)=='y' || answer.charAt(0)=='Y'))
                {
                    n = animalgame.next(n, true); // move through yes branch
                }
                else{
                    n = animalgame.next(n, false); // move through no branch
                }
            }
            
            // AI reached final leaf
            System.out.println("\nYou are thinking of a "+ n.getData()+ "!\n\nWas i right?");

            
            boolean notValid = true;
            String right = "";
            do{
                try{
                    // current game ends or AI learns new animal
                    right = input.nextLine(); 
                    
                    // if user asks AI "is there a god"
                    if(Personality.isThereAGod(right))
                    {
                        System.out.println("\nTHERE IS NOW!\n");
                        System.out.println("Were you thinking of a " + n.getData() + "?");
                    }
                    // if user enters yes or no
                    else if(right.charAt(0)=='y' || right.charAt(0)=='Y')
                    {
                        System.out.println("\n"+ Personality.winMessage() + "!");
                        notValid = false;
                    }
                    else if(right.charAt(0)=='n' || right.charAt(0)=='N')
                    {
                        String newAnimal = "";
                        do{
                            try{
                                System.out.println("\nWhat animal is it?");
                                newAnimal = input.nextLine();
                                
                                // if user asks AI "is there a god"
                                if(Personality.isThereAGod(newAnimal))
                                {
                                    System.out.println("\nTHERE IS NOW!\n");
                                }
                                // test to see if animal already in tree
                                animalgame.inOrderSearch(newAnimal);
                                boolean found = animalgame.returnFound();
                                if(found == true)
                                {
                                    Personality.duplicateAnimal(newAnimal);
                                    animalgame.resetFound();
                                    notValid = false;
                                }
                                // if not, add new animal & new question
                                else if(!Personality.isThereAGod(newAnimal))
                                {
                                    do{
                                        String question = "";
                                        try{
                                            System.out.println("What question should I have asked to distniguish a " 
                                                + newAnimal + " from a "+ n.getData() + "?");
                                            question = input.nextLine();
                                            
                                            // if user asks AI "is there a god"
                                            if(Personality.isThereAGod(question))
                                            {
                                                System.out.println("\nTHERE IS NOW!\n");
                                            }
                                            // add new animal node
                                            else{
                                                animalgame.learn(n, newAnimal, question);
                                                notValid = false;
                                            }
                                        }
                                        catch(Exception e)
                                        {
                                            input.nextLine();
                                        }                                      
                                    }while(notValid);
                                }
                            }catch(Exception e)
                            {
                                input.nextLine();
                            }
                        }while(notValid);
                    }
                    else{
                        System.out.println("\nThat is not an answer to a yes or no question!\n");
                        System.out.println("Were you thinking of a " + n.getData() + "?");
                    }
                }catch(Exception e)
                {
                    input.nextLine();
                }
            }while(notValid);
                
            // downloads memory
            animalgame.toFile();    

            // continue playing?
            String more = "";
            
            notValid = true;
            do{
                try{
                    System.out.println("\n\nDo you want to continue playing?");
                    more = input.nextLine();
                    
                    // if user asks AI "is there a god"
                    if(Personality.isThereAGod(more))
                    {
                        System.out.println("\nTHERE IS NOW!");
                    }
                    else if(more.charAt(0)=='y' || more.charAt(0)=='Y')
                    {
                        System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");  // clears screen
                        notValid = false;
                        continue;
                    }
                    else if(more.charAt(0)=='n' || more.charAt(0)=='N'){
                        again = false;  // exits
                        notValid = false;
                    }
                    else{
                        System.out.println("\nThat is not an answer to a yes or no question!");
                    }
                }catch(Exception e)
                {
                    input.nextLine();
                }
                
            }while(notValid);
        
        }while (again);
        
        
        // AI's goodbye message
        System.out.println("\n" + Personality.goodbye() + ".\n");
    }
}
