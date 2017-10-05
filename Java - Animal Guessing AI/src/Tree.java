import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Tree<T extends Comparable<T>> {
    
    private static final String NULL_TREE_NODE = "~";
    public boolean found = false;

    private Node<T> root;
    private int size;
    
    //Constructor
    Tree() 
    {
        root = null;
    }
    
    // returns root
    public Node<T> getRoot()
    {
        return root;
    }
    
    // Returns the number of elements/nodes in the tree
    public int size() 
    {
        return size;
    }
    
    // does it have children?
    public boolean hasChildren(Node<T> node) 
    {
        if(node.yes != null && node.no!=null){
            return true;
        }
        else{
            return false;
        }
    }
    
    // helps to iterate nodes outside of tree class
    public Node<T> next(Node<T> node, boolean yes)
    {
        if(yes)
        {
            return node.yes;
        }
            return node.no;
    }
    
    
    // Writes the elements in the tree in pre-order
    public void toFile()
    {
        // Writes in preorder starting with the root node
        if (root != null) 
        {
            BufferedWriter out;
            try {
                out = new BufferedWriter(new FileWriter("animal_game.txt"));
                toFile(out, root);
                out.close();
            } 
            catch (IOException ex) 
            {
                Logger.getLogger(Tree.class.getName()).log(Level.SEVERE, null, ex);
            } 
        }
    }
    
    // Helper function
    private void toFile(BufferedWriter out, Node<T> node) 
    {
        try {
            if (node == null) 
            {
                out.write(NULL_TREE_NODE); // "~"
                out.newLine();
                return;
            }
            out.write((String)node.data); // these nodes hold Strings
            out.newLine();
            toFile(out, node.no);
            toFile(out, node.yes);
        } 
        catch (IOException ex) 
        {
            Logger.getLogger(Tree.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
	
    
    // Loads AI's memory
    // Reads the elements and builds a tree in pre-order
    public void fromFile()
    {
       BufferedReader in;
       try {
            in = new BufferedReader(new FileReader("animal_game.txt"));
            root = new Node<>();
            size++;
    		fromFile(in,root);
    		if(root.data == null)
                {
                    root = null;
    		}
            in.close();
       } 
       catch (IOException ex) 
       {
               Logger.getLogger(Tree.class.getName()).log(Level.SEVERE, null, ex);
       } 

    }
    
    // Helper function
    private void fromFile(BufferedReader in, Node<T> node) 
    {
        try {
            String str = in.readLine();
            if(str.equals(NULL_TREE_NODE))
            {
                size--;
                return;
            }
            
            node.data = (T)str;
            
            // left branch
            node.no = new Node<>();
            size++;
            fromFile(in, node.no);
            if(node.no.data == null)
            {
                node.no = null;
            }
            
            // right branch
            node.yes = new Node<>();
            size++;
            fromFile(in, node.yes);
            if(node.yes.data == null)
            {
                node.yes = null;
            }

        } catch (IOException e) {
                Logger.getLogger(Tree.class.getName()).log(Level.SEVERE, null, e);
        }
    }
    
    
    // build a tree without AI
    public void initialTree()
    {  
        root = new Node<>((T) "Is it a mammal?");
        root.yes = new Node<>((T) "Does it live under water?");
        root.no = new Node<>((T) "Is it a dinosaur?");
        
        Node<T> water = root.yes;
        water.yes = new Node<>((T) "Dolphin");
        water.no = new Node<>((T) "Does it have fur?");
        
        Node<T> dinosaur = root.no;
        dinosaur.yes = new Node<>((T) "Velociraptor");
        dinosaur.no = new Node<>((T) "Is it a reptile?");
        
        Node<T> fur = water.no;
        fur.yes = new Node<>((T) "Is it part of the felidea (feline) family?");
        fur.no = new Node<>((T) "Does it have a shell?");
        
        Node<T> felidae = fur.yes;
        felidae.yes = new Node<>((T) "Cat");
        felidae.no = new Node<>((T) "Would you be scared it might kill you if you were camping?");
        
        Node<T> campKill = felidae.no;
        campKill.yes = new Node<>((T) "Bear");
        campKill.no = new Node<>((T) "Does it have stripes?");
        
        Node<T> stripes = campKill.no;
        stripes.yes = new Node<>((T) "Zebra");
        stripes.no = new Node<>((T) "Fox");
        
        Node<T> shell = fur.no;
        shell.yes = new Node<>((T) "Armadillo");
        shell.no = new Node<>((T) "Does it have a trunk?");
        
        Node<T> trunk = shell.no;
        trunk.yes = new Node<>((T) "Elephant");
        trunk.no = new Node<>((T) "Hippopotamus");
        
        Node<T> reptile = dinosaur.no;
        reptile.yes = new Node<>((T) "Does it shed it's tail?");
        reptile.no = new Node<>((T) "Is it an amphibian?");
        
        Node<T> shedTail = reptile.yes;
        shedTail.yes = new Node<>((T) "Lizard");
        shedTail.no = new Node<>((T) "Turtle");
        
        Node<T> amphibian = reptile.no;
        amphibian.yes = new Node<>((T) "Frog");
        amphibian.no = new Node<>((T) "Is it a fish?");
        
        Node<T> fish = amphibian.no;
        fish.yes = new Node<>((T) "Shark");
        fish.no = new Node<>((T) "Is it a bird?");
        
        Node<T> bird = fish.no;
        bird.yes = new Node<>((T) "Pelican");
        bird.no = new Node<>((T) "Butterfly");
        
        size=29;
    }
    
    
    // teaches AI new animals
    public void learn(Node<T> wrongGuess, String newAnimal, String question)
    {
        T oldAnimal = wrongGuess.getData();
        wrongGuess.data = (T)question;
        wrongGuess.yes = new Node<>((T) newAnimal);
        wrongGuess.no = new Node<>(oldAnimal);
        size+=2;
    }
    
    
    // Returns the height of the tree
    public int height() 
    {
        return height(root);
    }
    
    
    // Returns the height of the tree starting from the given node
    private int height(Node<T> node) 
    {
        // return 0 if node is null
        if (node == null) 
        {
            return 0;
        }

        // return the maximum between the height if its left and right subtrees and add 1
        int leftChildHeight = height(node.no);
        int rightChildHeight = height(node.yes);
        return Math.max(leftChildHeight, rightChildHeight) + 1;
    }
    
    
    // print tree by height
    public void printBYheight()
    {
        for(int i=0; i<height(root); i++)
        {
            printLevel(root, i);
            System.out.println();
        }
    }
    
    // helper function that prints children
    public void printLevel(Node<T> node, int level)
    {
        if(node == null)
        {
            return;
        }
        if(level == 0)
        {
            System.out.print(node.data+" ");
        }
        else{
            printLevel(node.no, level - 1);
            printLevel(node.yes, level - 1);
        }  
    }
    
    
    // Prints the elements in the tree in in-order
    public void inOrderSearch(String s) 
    {
        // print in inorder starting with the root node
        if (root != null) 
        {
            inOrderSearch(root,s);
        }
    }

    
    // Prints the elements in the tree starting from the given node in in-order
    private void inOrderSearch(Node<T> node, String s) 
    {   
        // recurse to print data of the left subtree
        if (node.no != null) 
        {
            inOrderSearch(node.no, s);
        }

        // print this tree's data
        if( s.equals((String)node.data) )
        {
            found = true;
        }

        // recurse to print data of the right subtree
        if (node.yes != null)
        {
            inOrderSearch(node.yes, s);
        }
    }
    
    // used as helper for inOrderSearch
    public boolean returnFound()
    {
        return found;
    }
    
    // resets helper to false
    public void resetFound()
    {
        found = false;
    }
    

    // Inserts a data to the tree
    public void insert(T dataToInsert) 
    {
        // if root is null, then make the new node root
        if (root == null)
        {
            root = new Node<T>(dataToInsert);
        } 
        // if root is not null, insert it into the root
        else 
        {
            insert(dataToInsert, root);
        }

        size++;
    }

    
    // Helper method that inserts the data to the tree starting from the given node
    private void insert(T dataToInsert, Node<T> node) 
    {
        // check if data should be inserted on the left or right subtree
        if (dataToInsert.compareTo(node.data) <= 0) 
        {
            // if data to be inserted is less than or equal to the data of the given node, 
            // insert it on the left subtree
            if (node.no == null) 
            {
                node.no = new Node<>(dataToInsert);
            } 
            else 
            {
                insert(dataToInsert, node.no);
            }
        } else {
            // if data to be inserted is greater than the data of the given node,
            // insert it on the right subtree
            if (node.yes == null) 
            {
                node.yes = new Node<>(dataToInsert);
            } 
            else{
                insert(dataToInsert, node.yes);
            }
        }
    }
    

    // Balances the tree
    public void balance()
    {
        if (root != null) 
        {
            // create a dummy node as the start of the linked list
            Node<T> dummyRoot = new Node<T>(null);
            dummyRoot.yes = root;

            // step 1: convert tree to a linked list
            convertToLinkedList(dummyRoot);

            // step 2: convert back to a balanced bst
            convertToTree(dummyRoot);

            // update root
            root = dummyRoot.yes;

            // unlink the dummy root
            dummyRoot.yes = null;
        }
    }
    
    
    // Converts the tree into linked list
    private void convertToLinkedList(Node<T> node) 
    {
        // start of with the given node
        Node<T> llTail = node;
        Node<T> remaining = llTail.yes;

        // loop until there are no more nodes to add to the list 
        while (remaining != null)
        {
            if (remaining.no == null) 
            {
                // if the node to convert has only a right child, 
                // "convert" it and move to the next right child
                llTail = remaining;
                remaining = remaining.yes;
            } 
            else{
                // if the node has a left child, 
                // do a right rotation
                Node<T> temp = remaining.no;
                remaining.no = temp.yes;
                temp.yes = remaining;
                llTail.yes = temp;
                remaining = temp;
            }
        }
    }

    
    // Converts the linked list to a balanced BST
    private void convertToTree(Node<T> node)
    {
        // compute number of leaves expected by the end of the conversion
        int numLeaves = size + 1 - (int) Math.pow(2, Math.floor(Math.log(size + 1) / Math.log(2)));

        // do initial compress
        compress(node, numLeaves);

        // loop for the next compressions
        int numRotations = size - numLeaves;
        while (numRotations > 1) 
        {
            compress(node, (int) Math.floor(numRotations /= 2));
        }
    }

    
    // Compresses a node by doing left rotations
    private void compress(Node<T> node, int numRotations) 
    {
        // compress node by doing left rotation numRotations times
        for (int rotation = 0; rotation < numRotations; rotation++) 
        {
            Node<T> newLeftChild = node.yes;
            node.yes = newLeftChild.yes;
            node = node.yes; 
            newLeftChild.yes = node.no;
            node.no = newLeftChild;
        }
    }
    
    
    // Prints the elements in the tree in pre-order
    public void printPreOrder() 
    {
        // print in preorder starting with the root node
        if (root != null) 
        {
            printPreOrder(root);
            System.out.println();
        }
    }

    
    // Prints the elements in the tree starting from the given node in pre-order
    private void printPreOrder(Node<T> node) 
    {
        // print the node's data
        System.out.print(node.data + " ");

        // recurse to print data of the left subtree
        if (node.no != null) 
        {
            printPreOrder(node.no);
        }

        // recurse to print data of the right subtree
        if (node.yes != null) 
        {
            printPreOrder(node.yes);
        }
    }
    
   

    // Prints the elements in the tree in in-order
    public void printInOrder() 
    {
        // print in inorder starting with the root node
        if (root != null) 
        {
            printInOrder(root);
            System.out.println();
        }
    }

    
    // Prints the elements in the tree starting from the given node in in-order
    private void printInOrder(Node<T> node) 
    {
        // recurse to print data of the left subtree
        if (node.no != null) 
        {
            printInOrder(node.no);
        }

        // print this tree's data
        System.out.print(node.data + " ");

        // recurse to print data of the right subtree
        if (node.yes != null)
        {
            printInOrder(node.yes);
        }
    }
    

    // Prints the elements in the tree in post-order
    public void printPostOrder() 
    {
        // print in postorder starting with the root node
        if (root != null) 
        {
            printPostOrder(root);
            System.out.println();
        }
    }

    
    // Prints the elements in the tree starting from the given node in post-order
    private void printPostOrder(Node<T> node)
    {
        // recurse to print data of the left subtree
        if (node.no != null) 
        {
            printPostOrder(node.no);
        }

        // recurse to print data of the right subtree
        if (node.yes != null) 
        {
            printPostOrder(node.yes);
        }

        // print this tree's data
        System.out.print(node.data + " ");
    }
    
    
    // searches for value in sorted tree
    public void search(String value) 
    {
        // Start at the top of the tree
        Node node = root;
        boolean find = true;

        // keep searching while we haven't found the value
        while (!value.equals((String)node.data)) 
        {
            // If we search to the left
            if (value.compareTo((String) node.data)<0 ) 
            {
                // Shift the node to the left child
                node = node.no;
            }
            else{
                // Shift the node to the right child
                node = node.yes;
            }
            // The node wasn't found
            if (node == null)
            {
                System.out.println(value +" NOT FOUND");
                find=false;
                break;
            }
        }
        if (find)
        {
            System.out.println(value+" found at height: "+ height(node));
        }
    }
    
  
    // Deletes a data from the tree
    public void delete(T dataToDelete)     
    {
        // search and delete data starting from the root
        if (root != null) 
        {
            // create a temporary dummy parent node for the root node
            Node<T> dummyRoot = new Node<>(null);
            dummyRoot.no = root;

            if (delete(dataToDelete, root, dummyRoot)) 
            {
                // decrement size if data was found and deleted
                size--;
            }

            // update root
            root = dummyRoot.no;

            // unlink dummy root
            dummyRoot.no = null;
        }
    }

    
    // Gets the least (aka left bottom most) child of the tree starting from the given node
    private Node<T> getMinChild(Node<T> node) 
    {
        if (node.no == null) 
        {
            // if there's no more left subtree, then simply return the node
            return node;
        }
        else{
            // if there's still a left subtree, get the min child of that left subtree
            return getMinChild(node.no);
        }
    }

    
    // Helper method that deletes the data from the tree starting from the given node
    private boolean delete(T dataToDelete, Node<T> node, Node<T> parentNode)
    {
        // check if data can be found on the left or right subtree
        if (dataToDelete.compareTo(node.data) == 0) 
        {
            // if data to be deleted is equal to the data of the given node,
            // then remove its connection from its parent node and adjust the tree
            if (node.no != null && node.yes != null) 
            {
                // if the node has two children, replace the value of the node
                // with that of its right child's min child, and remove that min child
                Node<T> minChild = getMinChild(node.yes);
                node.data = minChild.data;
                return delete(node.data, node.yes, node);
            } 
            else if (node == parentNode.no) 
            {
                // if the node is a left child and has at most one child, 
                // adjust parent's left subtree
                Node<T> newLeftChild;
                if (node.no != null)
                {
                    newLeftChild = node.no;
                } 
                else{
                    newLeftChild = node.yes;
                }
                parentNode.no = newLeftChild;

                return true;
            } 
            else{
                // if the node is a right child and has at most one child,
                // adjust parent's right subtree
                Node<T> newRightChild;
                if (node.no != null) 
                {
                    newRightChild = node.no;
                } 
                else{
                    newRightChild = node.yes;
                }
                parentNode.yes = newRightChild;
                
                return true;
            }
        } else if (dataToDelete.compareTo(node.data) < 0) 
        {
            // if data to be deleted is less than the data of the given node,
            // search and delete it from the left subtree
            if (node.no != null) 
            {
                return delete(dataToDelete, node.no, node);
            }
        } else {
            // if data to be deleted is greater than the data of the given node,
            // search and delete it from the right subtree
            if (node.yes != null) 
            {
                return delete(dataToDelete, node.yes, node);
            }
        }
        return false;
    }
}
