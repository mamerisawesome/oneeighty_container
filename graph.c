// [REFERENCE] http://www.geeksforgeeks.org/graph-and-its-representations/

#include "graph.h"



int main() {
    int V = 8;
    struct Graph* graph = createGraph(V);
    addEdge(graph, 0, 1);
    addEdge(graph, 0, 2);
    addEdge(graph, 0, 3);
    addEdge(graph, 1, 4);
    addEdge(graph, 1, 2);
    addEdge(graph, 2, 4);
    addEdge(graph, 2, 3);
    addEdge(graph, 2, 7);
    addEdge(graph, 2, 5);
    addEdge(graph, 3, 7);
    addEdge(graph, 4, 5);
    addEdge(graph, 5, 6);
    addEdge(graph, 6, 7);

    printGraph(graph);
 
    return 0;
}