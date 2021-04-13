#ifndef ASTAR_H
#define ASTAR_H

#include <iostream>
#include <math.h>

const int MAX_G = 100000000;

struct Node
{
    int x;          //x coordinate
    int y;          //y coordinate
    int f;          //Sum of g and h values
    int g;          //Distance from start node
    int h;          //Distance from finish node using heuristic
    int position;   //Position in min heap
    bool open;
    Node * parent = NULL;
};

int calcdist(Node * n1, Node * n2){                //Heuristic value calculator using euclidean distance
    int diffx = (n2->x - n1->x)*(n2->x - n1->x);
    int diffy = (n2->y - n1->y)*(n2->y - n1->y);
    int dist = 10*sqrt(diffx + diffy);
    //cout<<"Calculated dist: "<<dist<<endl;
    return dist;
};

void getadj(int arrx[], int arry[], Node* n){
    int k = 0;
    for (int i = -1; i < 2; i++)
    {
        arrx[k] = n->x + i;
        arry[k] = n->y + i;
        k++;
    }

};

#endif