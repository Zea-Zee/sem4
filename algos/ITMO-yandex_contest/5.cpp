#include "Network.h"
#include <iostream>
#include <vector>

using namespace std;

int main(int argc, char* argv[]){
    int m;
    cin >> m;

    vector<Edge> edges(m);
    for(int i = 0; i < m; i++){
        cin >> edges[i].id >> edges[i].i >> edges[i].j;
    }
    Network network(edges);

    for(int i = 0; i < m + 1; i++){
        for(int j = 0; j < m + 1; j++){
            Path path = network.getPath(i, 0);
            if(path.isContaminated){
                network.printPath(path);
                return 0;
            }
        }
    }
}
