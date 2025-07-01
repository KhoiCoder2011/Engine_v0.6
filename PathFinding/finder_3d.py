import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y, z)
        self.parent = parent
        self.g = 0  # Cost from start node
        self.h = 0  # Heuristic cost to end node
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f  # Priority queue comparison

def heuristic(a, b):
    """Heuristic function using Manhattan distance in 3D"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def a_star_3d(grid, start, end):
    """A* algorithm in a 3D grid"""
    open_list = []
    closed_set = set()

    start_node = Node(start)
    end_node = Node(end)
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)  # Get node with lowest f-score

        if current_node.position == end:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path (start to end)

        closed_set.add(current_node.position)

        # Possible movements in 3D: left, right, forward, backward, up, down
        neighbors = [
            (1, 0, 0), (-1, 0, 0),  # Left, Right
            (0, 1, 0), (0, -1, 0),  # Forward, Backward
            (0, 0, 1), (0, 0, -1)   # Up, Down
        ]

        for move in neighbors:
            neighbor_pos = (
                current_node.position[0] + move[0],
                current_node.position[1] + move[1],
                current_node.position[2] + move[2]
            )

            if (0 <= neighbor_pos[0] < len(grid) and
                0 <= neighbor_pos[1] < len(grid[0]) and
                0 <= neighbor_pos[2] < len(grid[0][0]) and
                grid[neighbor_pos[0]][neighbor_pos[1]][neighbor_pos[2]] == 0 and
                neighbor_pos not in closed_set):

                neighbor_node = Node(neighbor_pos, current_node)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = heuristic(neighbor_pos, end_node.position)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                heapq.heappush(open_list, neighbor_node)

    return None  # No path found

# --- Example 3D Grid ---
grid_3d = [
    [  # Layer 0 (Ground level)
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0]
    ],
    [  # Layer 1
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ],
    [  # Layer 2
        [0, 0, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
]

start = (0, 0, 0)  # (x, y, z)
end = (2, 2, 2)    # (x, y, z)

path = a_star_3d(grid_3d, start, end)
print("Path found:", path)
