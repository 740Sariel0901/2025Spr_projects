import random
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import time
from assign_value import assign_value
import solver_final

def draw_graph(G, positions, start, end, gray, title, highlight_edges=None):
    """
    Common drawing function.

    Parameters:
    - G: The graph to be drawn.
    - positions: A dictionary with node positions.
    - start, end: The start and end nodes (used for coloring nodes red and green).
    - title: Title of the graph.
    - highlight_edges: Optional list of edges to draw in blue, thick.
    """
    plt.figure(figsize=(6, 6))
    labels = {node: f"{node}\n{G.nodes[node]['value']}" for node in G.nodes()}
    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append("red")
        elif node == end:
            node_colors.append("green")
        elif node in gray:
            node_colors.append("gray")
        else:
            node_colors.append("skyblue")

    nx.draw_networkx_nodes(G, pos=positions, node_color=node_colors, node_size=500)
    nx.draw_networkx_labels(G, pos=positions, labels=labels, font_size=7)

    if highlight_edges:
        highlight_set = set(highlight_edges)
        normal = [
            e for e in G.edges()
            if e not in highlight_set and (e[1], e[0]) not in highlight_set
        ]
        nx.draw_networkx_edges(G, pos=positions, edgelist=normal, edge_color="gray")
        nx.draw_networkx_edges(G, pos=positions, edgelist=highlight_edges,
                               edge_color="blue", width=3)
    else:
        nx.draw_networkx_edges(G, pos=positions, edge_color="gray")

    plt.title(title)
    plt.axis("off")
    plt.show()

# Generate path and gray randomly
class Path_and_Gray():
    def __init__(self, n):
        self.n = n  # define the board size
        self.board = [['X' for _ in range(n)] for _ in range(n)]
        self.priority = random.sample(range(1, self.n + 1), self.n)
        self.G = nx.Graph()
        self.positions = {}
        self.neighbor_direction = [(-1, 0), (0, 1), (1, 1), (1, 0), (0, -1), (-1, -1)]
        self.gray = []

    def choose_start_and_end(self):
        """This function choose where to start and end randomly."""
        place = ['left', 'right', 'up', 'down']
        start = random.choice(place)
        start_row = random.randint(0, self.n - 1)
        start_col = random.randint(0, self.n - 1)
        end_row = random.randint(0, self.n - 1)
        end_col = random.randint(0, self.n - 1)
        if start == 'left':
            self.start = (start_row, 0)
            self.end = (end_row, self.n - 1)
        elif start == 'right':
            self.start = (start_row, self.n - 1)
            self.end = (end_row, 0)
        elif start == 'up':
            self.start = (0, start_col)
            self.end = (self.n - 1, end_col)
        else:
            self.start = (self.n - 1, start_col)
            self.end = (0, end_col)
        return self.start, self.end

    def paraphase_to_graph(self):
        for row in range(self.n):
            for col in range(self.n):
                node = (row, col)
                value = self.board[row][col]
                self.G.add_node(node, value=value)
                self.positions[node] = (col - 0.5 * row, -row)
        for row in range(self.n):
            for col in range(self.n):
                node = (row, col)
                for d in self.neighbor_direction:
                    nr = row + d[0]
                    nc = col + d[1]
                    if 0 <= nr < self.n and 0 <= nc < self.n:
                        neighbor = (nr, nc)
                        self.G.add_edge(node, neighbor)
        return self.G

    def draw(self, title):
        draw_graph(self.G, self.positions, self.start, self.end, self.gray, title)

    def set_a_path(self):
        """
        Build a path from 'self.start' to 'self.end' by random exploration,
        backtracking on dead ends, and avoiding revisiting failed branches.
        Ensures each path node has at most two neighbors on the path.
        """
        self.path = [self.start]
        # Track which next-nodes have been tried at each node
        tried = {self.start: set()}

        while self.path:
            current = self.path[-1]
            # If we've reached the end node, return the path
            if current == self.end:
                return self.path

            # Initialize tried set for the current node if not present
            if current not in tried:
                tried[current] = set()

            # Gather neighbors that haven't been visited and not yet tried
            raw_candidates = [
                neighbor
                for neighbor in self.G.neighbors(current)
                if neighbor not in self.path and neighbor not in tried[current]
            ]

            # Filter out candidates that would cause any node to have
            # more than two neighbors within the prospective path
            candidates = []
            for neighbor in raw_candidates:
                prospective_path = self.path + [neighbor]
                valid = True
                for node in prospective_path:
                    # Count how many neighbors of node are in the path
                    count = sum(1 for nb in self.G.neighbors(node) if nb in prospective_path)
                    if count > 2:
                        valid = False
                        break
                if valid:
                    candidates.append(neighbor)

            if candidates:
                # Randomly select a new neighbor, mark it as tried, and advance
                next_node = random.choice(candidates)
                tried[current].add(next_node)
                self.path.append(next_node)
            else:
                # No valid extensions, backtrack
                tried.pop(current, None)
                self.path.pop()

        # No path found after backtracking completely
        raise RuntimeError("No path found from start to end")

    def valid_path(self, path):
        """Generate a path that has at least n-1 nodes that each of them has at least 1 node not on the path"""
        nodes_count = 0
        for node in path:
            neighbors = [nbr for nbr in self.G.neighbors(node) if nbr not in path]
            if len(neighbors) > 1:
                nodes_count += 1
        if nodes_count >= self.n - 1:
            return True
        else:
            return False

    def generate_valid_path(self):
        while True:
            self.set_a_path()
            if self.valid_path(self.path):
                return self.path

    def select_gray(self):
        gray_num = int(self.n / 2)
        for i in range(gray_num):
            gray = random.choice([node for node in self.path if node != self.start and node != self.end])
            self.gray.append(gray)
        return self.gray



# Search for all possible paths and priority for this puzzle
class SearchAll:
    def __init__(self, G, start, end, gray, neighbor_direction, positions):
        self.G = G
        self.start = start
        self.end = end
        self.gray = gray
        solver = solver_final.PuzzleSolver(G, start, end, gray, neighbor_direction, positions)
        self.all_priorities = solver.pruning_strategy()

    def choose_a_move(self, node, priority, visited_node):
        available_neighbors = [
            node
            for node in self.G.neighbors(node)
            if node not in visited_node
               and isinstance(self.G.nodes[node]['value'], int)
        ]
        if node in self.gray:
            priority = priority[::-1]
        for value in priority:
            # Only add neighbor n if its value matches the current priority value
            # and n is not already visited.
            valid_moves = [n for n in available_neighbors if self.G.nodes[n]['value'] == value]
            if valid_moves:
                return valid_moves
        return []

    def find_all_valid_paths(self):
        self.all_paths = []
        for priority in self.all_priorities:
            visited_node = [self.start]
            current_node = self.start
            while True:
                if current_node != self.end:
                    valid_moves = self.choose_a_move(current_node, priority, visited_node)
                    if len(valid_moves) != 1:
                        break
                    current_node = valid_moves[0]
                    visited_node.append(current_node)
                else:
                    valid_moves = self.choose_a_move(current_node, priority, visited_node)
                    if len(valid_moves) != 1:
                        self.all_paths.append(visited_node)
                        # print("path: ", visited_node)
                        # print("priority:", priority)
                        break
                    else:
                        break
        self.all_paths = [list(p) for p in {tuple(p) for p in self.all_paths}]
        return self.all_paths




# Change the “divergence” (fork) node back to 'X' or other value
class Unique():
    def __init__(self, path, all_paths, G):
        self.path = path
        self.all_paths = all_paths
        self.G = G

    def change_to_X(self):
        out_path_node = set([node for row in self.all_paths for node in row])
        # print(out_path_node)
        for node in out_path_node:
            if node not in self.path:
                # print(node)
                self.G.nodes[node]['value'] = "X"
        return self.G


def Generator():
    # 1) Randomly generate path, priority, start point, end point, and gray nodes
    PnG = Path_and_Gray(7)
    neighbor_direction = PnG.neighbor_direction
    positions         = PnG.positions
    priority          = PnG.priority

    print("priority:", priority)
    PnG.choose_start_and_end()
    orig_G = PnG.paraphase_to_graph()
    PnG.generate_valid_path()
    path = PnG.path
    print("target path:", path)
    PnG.select_gray()
    start, end, gray = PnG.start, PnG.end, PnG.gray

    # 2) Retry the assignment until only one valid remaining path is left
    while True:
        # Copy the original graph so we don't modify it directly
        G = orig_G.copy()
        try:
            G = assign_value(G, priority, path, start, end, gray, n=7)
        except (StopIteration, ValueError, IndexError) as e:
            print(f"[retry] assignment failed ({e}), retrying…")
            time.sleep(0.1)
            continue

        # Draw the current graph with the chosen path highlighted
        for u, v in zip(path, path[1:]):
            G.add_edge(u, v, path='path')
        edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('path') == 'path']
        draw_graph(
            G, positions, start, end, gray,
            title="Graph Visualization",
            highlight_edges=edges
        )

        # ① Find all possible paths under current numbering
        SA = SearchAll(G, start, end, gray, neighbor_direction, positions)
        all_paths = SA.find_all_valid_paths()
        print('all_paths:', all_paths)

        # ② Block off all nodes not on the main path
        U = Unique(path, all_paths, G)
        final_G = U.change_to_X()

        # ③ Re-run search to see how many paths remain
        SA2 = SearchAll(final_G, start, end, gray, neighbor_direction, positions)
        remaining = SA2.find_all_valid_paths()
        print('remaining:', remaining)

        # If exactly one path remains, return everything needed for final drawing
        if len(remaining) == 1:
            return final_G, remaining, positions, start, end, gray, edges
        # Otherwise, retry with a fresh assignment

if __name__ == '__main__':
    final_G, remaining, positions, start, end, gray, edges = Generator()
    # Draw the final puzzle only once, when exactly one path remains
    draw_graph(
        final_G, positions, start, end, gray,
        title='Final Puzzle',
        highlight_edges=edges
    )

