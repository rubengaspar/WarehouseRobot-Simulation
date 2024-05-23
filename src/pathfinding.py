import heapq

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.cell import Cell
    from src.grid import Grid
    from src.position import Position


def get_neighbours(cell: 'Cell'):
    return cell.connections


def heuristic(start: 'Position', destination: 'Position'):
    # Manhattan distance heuristic
    return abs(start.x - destination.x) + abs(start.y - destination.y)


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


class Pathfinding:
    def __init__(self, grid: 'Grid'):
        self.grid = grid

    def a_star(self, start: 'Position', destination: 'Position'):
        start_cell = self.grid.get_cell(start)
        destination_cell = self.grid.get_cell(destination)

        open_set = []
        heapq.heappush(open_set, (0, start_cell))
        came_from = {}
        g_score = {start_cell: 0}
        f_score = {start_cell: heuristic(start, destination)}
        close_set = []

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == destination_cell:
                return reconstruct_path(came_from, current)

            close_set.append(current)

            neighbors = get_neighbours(current)

            for connection in neighbors:
                neighbor = connection.to_cell
                if neighbor in close_set:
                    continue
                tentative_g_score = g_score[current] + connection.weight

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor.position, destination)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    # def dijkstra(self, start, destination):
    #     """
    #     :param start: The starting node for Dijkstra's algorithm.
    #     :param destination: The destination node for Dijkstra's algorithm.
    #     :return: The shortest path from the start node to the goal node.
    #
    # This method implements Dijkstra's algorithm to find the shortest path from the start node to the goal node in a
    # graph. It takes two parameters, `start` and `goal`, which represent the * starting node and the goal node
    # respectively. The method returns the shortest path from the start node to the goal node as a list of nodes.
    #
    # The algorithm works as follows: 1. Initialize an empty `open_set` priority queue. 2. Push the starting node
    # with a priority of 0 into the `open_set`. 3. Initialize an empty `came_from` dictionary to keep track of the
    # shortest path. 4. Initialize a `g_score` dictionary to keep track of the cost of reaching each node from the
    # start node. 5. While the `open_set` is not empty: - Pop the node with the lowest priority from the `open_set`.
    # This becomes the current node. - If the current node is the goal node, return the reconstructed path using the
    # `came_from` dictionary. - Get the neighbors of the current node. - For each neighbor of the current node: -
    # Calculate the tentative `g_score` by adding the cost of reaching the current node and the distance between the
    # current node and the neighbor. - If the neighbor is not in `g_score` or the tentative `g_score` is lower than
    # the current `g_score` of the neighbor: - Update `came_from` with the current node as the parent of the
    # neighbor. - Update the `g_score` of the neighbor with the tentative `g_score`. - Push the neighbor into the
    # `open_set` with the new `g_score` as the priority. 6. If the algorithm completes without finding a path to the
    # goal, return an empty list.
    #
    #     Example usage:
    #     start = Node("A")
    #     goal = Node("B")
    #     path = dijkstra(graph, start, goal)
    #     print(path)
    #
    # Note: This method assumes the existence of helper methods `reconstruct_path()` and `get_neighbors()` which are
    # not provided here.
    #
    #     """
    #     open_set = []
    #     heapq.heappush(open_set, (0, start))
    #     came_from = {}
    #     g_score = {start: 0}
    #
    #     while open_set:
    #         current = heapq.heappop(open_set)[1]
    #
    #         if current == destination:
    #             return reconstruct_path(came_from, current)
    #
    #         neighbors = get_neighbours(current)
    #
    #         for neighbor in neighbors:
    #             tentative_g_score = g_score[current] + 1
    #
    #             if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
    #                 came_from[neighbor] = current
    #                 g_score[neighbor] = tentative_g_score
    #                 heapq.heappush(open_set, (g_score[neighbor], neighbor))
    #
    #     return []
    #
    # def bfs(self, start, destination):
    #     """
    #     Perform a Breadth-First Search (BFS) algorithm to find the shortest path from a given start node to a goal node.
    #
    #     :param start: The starting node.
    #     :param destination: The goal node.
    #     :return: A list representing the shortest path from start to goal. If no path is found, an empty list is returned.
    #     """
    #     queue = deque([start])
    #     came_from = {start: None}
    #
    #     while queue:
    #         current = queue.popleft()
    #
    #         if current == destination:
    #             return reconstruct_path(came_from, current)
    #
    #         neighbors = get_neighbours(current)
    #
    #         for neighbor in neighbors:
    #             if neighbor not in came_from:
    #                 queue.append(neighbor)
    #                 came_from[neighbor] = current
    #
    #     return []
    #
    # def dfs(self, start, destination):
    #     """
    #     :param start: The starting node for the depth-first search.
    #     :param destination: The goal node that we are trying to reach.
    #     :return: A list containing the path from the start node to the goal node.
    #
    #     The depth-first search (DFS) algorithm is used to traverse a graph or a tree structure. It starts from a given node (start) and explores all of its neighbors before moving on to their
    #     * neighbors. This process continues until the goal node is reached or until there are no more unexplored nodes available.
    #
    #     The DFS method takes the start and goal nodes as parameters and returns a list representing the path from the start node to the goal node. If no path is found, an empty list is returned
    #     *.
    #
    #     Example usage:
    #
    #     start = Node(1)
    #     goal = Node(5)
    #     path = dfs(start, goal)
    #
    #     In this example, we start the DFS search from node 1 and try to reach node 5. The result will be a list that represents the path from node 1 to node 5 if a path exists, or an empty list
    #     * if no path is found.
    #     """
    #     stack = [start]
    #     came_from = {start: None}
    #
    #     while stack:
    #         current = stack.pop()
    #
    #         if current == destination:
    #             return reconstruct_path(came_from, current)
    #
    #         neighbors = get_neighbours(current)
    #
    #         for neighbor in neighbors:
    #             if neighbor not in came_from:
    #                 stack.append(neighbor)
    #                 came_from[neighbor] = current
    #
    #     return []
    #
    # def greedy_best_first(self, start, destination):
    #     """
    #     :param start: The starting state of the search.
    #     :param destination: The target state to search for.
    #     :return: A list representing the path from the start state to the goal state, if a path exists. Otherwise, an empty list.
    #
    #     This method performs a greedy best-first search to find the path from the start state to the goal state. It utilizes a priority queue to prioritize states based on their heuristic values
    #     *, which estimate the cost to reach the goal state.
    #     The algorithm starts with an empty priority queue `open_set` and adds the start state to it with a priority value equal to the heuristic value of the start state. It also initializes
    #     * an empty dictionary `came_from` to keep track of the previous state that leads to each state.
    #
    #     While there are states in the `open_set`, the algorithm continues to explore states. It pops the state with the lowest priority value from the `open_set` using `heapq.heappop()` and
    #     * assigns it to the variable `current`.
    #     If `current` is equal to the goal state, the algorithm calls the `reconstruct_path()` method to retrieve the path from the start state to the goal state using `came_from` dictionary
    #     *, and returns the path.
    #
    #     If `current` is not equal to the goal state, the algorithm retrieves the neighbors of `current` using the `self.get_neighbors()` method. It iterates over each neighbor and if it has
    #     * not been visited before (i.e., not in the `came_from` dictionary), it assigns the current state as its previous state in `came_from` and adds it to the `open_set` with a priority value
    #     * equal to the heuristic value of the neighbor.
    #
    #     If the algorithm completes its search without finding the goal state, it returns an empty list to indicate that no valid path exists.
    #     """
    #     open_set = []
    #     heapq.heappush(open_set, (heuristic(start, destination), start))
    #     came_from = {}
    #
    #     while open_set:
    #         current = heapq.heappop(open_set)[1]
    #
    #         if current == destination:
    #             return reconstruct_path(came_from, current)
    #
    #         neighbors = get_neighbours(current)
    #
    #         for neighbor in neighbors:
    #             if neighbor not in came_from:
    #                 came_from[neighbor] = current
    #                 heapq.heappush(open_set, (heuristic(neighbor, destination), neighbor))
    #
    #     return []
