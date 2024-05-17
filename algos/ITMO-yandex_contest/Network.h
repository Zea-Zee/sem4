#include <vector>


struct Path
{
    std::vector<int> path = {};
    bool isContaminated = false;
};

struct Edge
{
    int id, i, j;
};

class Network
{
    public:
        Network(const std::vector<Edge> edges);
        Path getPath(int source, int dest);
        void printPath(Path path);
    private:
        int n;
        std::vector<Edge> edges;
        std::vector<std::vector<int>> adj;
        Path BFS(int source, int dest);
};
