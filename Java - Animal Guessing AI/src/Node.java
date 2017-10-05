public class Node<T extends Comparable<T>>  
{
    // The data the node holds
    public T data;

    // The left child of the node
    public Node<T> no;

    // The right child of the node
    public Node<T> yes;

    // constructor
    public Node() 
    {
        data = null;
        no = yes = null;
    }

    // Instantiates a new node with the given data.
    Node(T data) 
    {
        this.data = data;
    }

    // returns data inside node
    public T getData()
    {
        return data;
    }
}
