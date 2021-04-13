#include <iostream>
#include "myHeap.h"
#include "astar.h"
#include <fstream>

using namespace std;


int main(){

    ifstream file;
    string filename, row;
    filename = "graph.txt";
    file.open(filename);

//Getting first row
    getline(file, row);

//Getting row size
    int N = row.length() - 1;                       // -1 because the text file has a space after every last number on each line
    int graph[N+2][N+2] = { }, rownum = 1;          // Setting matrix to be N+2 dimensions to set a border around the maze
    
    for (int i = 1; i < N+1; i++)
    {
        graph[rownum][i] = row[i-1] - 48;            // Makig first row
    }
    rownum++;
//Getting the rest of the rows
    while (getline(file, row))                      //Opening file and creating 2D array from graph.txt
    {
        for (int i = 1; i < N+1; i++)
        {
            graph[rownum][i] = row[i-1] - 48;
        }
        
        rownum++;
    }
    file.close();


//Initialization 
    Heap<Node> *myheap = new Heap<Node>; 
    Node *elements[10000];

    Node * start = new Node;
    Node * finish = new Node;

    start->x = 1;
    start->y = 1;
    finish->x = N;
    finish->y = N;
    start->g = 0;
    finish->h = 0;
    start->h = calcdist(start, finish);
    finish->g = start->h;
    finish->f = finish->g;
    start->f = start->h;
    start->open = false;

    myheap->insert(start);
    //elements[0] = start;
    int num = 0;
    int loop = 0;

    while (!myheap->IsEmpty())
    {
        Node * current = myheap->remove_min();
        //cout<<"In first while\n";
        current->open = false;
        elements[num++] = current;


        if (current->x == finish->x && current->y == finish->y)         //Check if final node reached
        {
            Node *n = current;
            while (n != NULL)
            {
                cout<<n->x<<" "<<n->y<<endl;
                n = n->parent;
            }
            
            for (int i = 0; i < num; i++)
            {
                delete elements[i];
            }
            delete myheap;
            cout<<"Path found\n";
            return 0;
        }
        
        int arrx[3], arry[3];

        getadj(arrx, arry, current);            //Gets adjacent nodes to current

        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                if (i == 1 && j == 1)           //To not check for same node
                {
                    continue;
                }
                if (graph[arrx[i]][arry[j]] == 0)            //Check if free space 
                {
                    continue;
                }

                
                Node temp;
                temp.x = arrx[i];
                temp.y = arry[j];

                bool inlist = false;
                for (int l = 0; l < num; l++)           //Checks if node was visited before and was removed from heap earlier, avoids gettin stuck in loop;
                {
                    if (elements[l] != NULL && elements[l]->x == temp.x && elements[l]->y == temp.y)
                    {
                        inlist = true;
                        break;
                    }
                }
                if (inlist)
                {
                    continue;
                }

                Node * temp_ptr = myheap->searchnode(temp);     //Search for node in queue
                //cout<<"Searched node: "<<temp.x<<" "<<temp.y<<endl;
                bool inheap = true;

                if (temp_ptr == NULL)           //If node not in queue initialize node
                {
                    
                    temp_ptr = new Node;
                    temp_ptr->x = temp.x;
                    temp_ptr->y = temp.y;
                    temp_ptr->f = MAX_G;
                    temp_ptr->g = MAX_G;
                    temp_ptr->h = calcdist(temp_ptr, finish);
                    temp_ptr->parent = current;
                    inheap = false;
                }

                if (temp_ptr->g > current->g + calcdist(temp_ptr, current))     //check if dist fom start to temp is > start to current to temp
                {
                    temp_ptr->g = current->g + calcdist(temp_ptr, current);
                    temp_ptr->parent = current;
                    if (inheap)
                    {
                        myheap->decreaseKey(temp_ptr->position, temp_ptr->g + temp_ptr->h);
                    }
                    else
                    {
                        temp_ptr->f = temp_ptr->g + temp_ptr->h;
                        myheap->insert(temp_ptr);
                    }
                    
                }
                
            }
            
        }
        
        if (loop > pow(N,2))        //Error checking
        {
            //myheap->printarr();
            cout<<"path does not exists"<<endl;
            return -1;
        }
        loop++;
        

    }
    



    return 0;
}