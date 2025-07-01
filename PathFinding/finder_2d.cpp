#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <set>
#include <tuple>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace std;

class Node
{
public:
    tuple<int, int> position;
    Node *parent;
    int g, h, f;

    Node(tuple<int, int> pos, Node *parentNode = nullptr)
        : position(pos), parent(parentNode), g(0), h(0), f(0) {}

    bool operator<(const Node &other) const
    {
        return f > other.f;
    }
};

int heuristic(tuple<int, int> a, tuple<int, int> b)
{
    return abs(get<0>(a) - get<0>(b)) + abs(get<1>(a) - get<1>(b));
}

vector<tuple<int, int>> a_star_search(vector<vector<int>> &grid, tuple<int, int> start, tuple<int, int> end)
{
    priority_queue<Node> open_list;
    set<tuple<int, int>> closed_set;

    Node *start_node = new Node(start);
    Node *end_node = new Node(end);

    open_list.push(*start_node);

    vector<tuple<int, int>> neighbors = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}};
    vector<tuple<int, int>> path;

    while (!open_list.empty())
    {
        Node *current_node = new Node(open_list.top());
        open_list.pop();

        if (current_node->position == end)
        {
            while (current_node != nullptr)
            {
                path.push_back(current_node->position);
                current_node = current_node->parent;
            }
            reverse(path.begin(), path.end());
            return path;
        }

        closed_set.insert(current_node->position);

        for (auto &move : neighbors)
        {
            tuple<int, int> neighbor_pos = {get<0>(current_node->position) + get<0>(move), get<1>(current_node->position) + get<1>(move)};
            int x = get<0>(neighbor_pos), y = get<1>(neighbor_pos);

            if (x >= 0 && x < grid.size() && y >= 0 && y < grid[0].size() && grid[x][y] == 0 && closed_set.find(neighbor_pos) == closed_set.end())
            {
                Node *neighbor_node = new Node(neighbor_pos, current_node);
                neighbor_node->g = current_node->g + 1;
                neighbor_node->h = heuristic(neighbor_pos, end);
                neighbor_node->f = neighbor_node->g + neighbor_node->h;

                open_list.push(*neighbor_node);
            }
        }
    }

    return {};
}

vector<tuple<int, int>> a_star_search_wrapper(vector<vector<int>> &grid, tuple<int, int> start, tuple<int, int> end)
{
    return a_star_search(grid, start, end);
}

PYBIND11_MODULE(finder_2d, m)
{
    m.def("a_star_search", &a_star_search_wrapper, "A* algorithm to find a path", py::arg("grid"), py::arg("start"), py::arg("end"));
}