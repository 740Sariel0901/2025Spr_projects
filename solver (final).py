import matplotlib.pyplot as plt
import networkx as nx
import itertools
import collections


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



class Board():
    def __init__(self, input_board):
        self.input_list = input_board['input_list']
        self.size = len(self.input_list)
        self.start = input_board['start']
        self.end = input_board['end']
        self.gray = input_board['gray'] or []
        self.neighbor_direction = [(-1, 0), (0, 1), (1, 1), (1, 0),
                                   (0, -1), (-1, -1)]
        self.G = nx.Graph()
        self.positions = {}

    def parse_board(self):
        for r in range(self.size):
            for c in range(self.size):
                node = (r, c)
                val = self.input_list[r][c]
                self.G.add_node(node, value=val)
                self.positions[node] = (c - 0.5 * r, -r)
        for r in range(self.size):
            for c in range(self.size):
                for dr, dc in self.neighbor_direction:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        self.G.add_edge((r, c), (nr, nc))
        return self.G

    def draw(self):
        draw_graph(self.G, self.positions, self.start, self.end,
                   self.gray, "Initial Board")


class PuzzleSolver():
    def __init__(self, input_board):
        B = Board(input_board)
        self.solution_G = B.parse_board()
        self.start = B.start
        self.end = B.end
        self.gray = B.gray
        self.neighbor_direction = B.neighbor_direction
        self.positions = B.positions
        # collect distinct numeric values
        nums = {
            self.solution_G.nodes[n]['value']
            for n in self.solution_G.nodes()
            if isinstance(self.solution_G.nodes[n]['value'], int)
        }
        self.priority = list(itertools.permutations(nums))
        self.path = []

    def pruning_strategy(self):
        """Your existing pruning logic (unchanged)."""
        start_vals = [self.solution_G.nodes[n]['value']
                      for n in self.solution_G.neighbors(self.start)
                      if isinstance(self.solution_G.nodes[n]['value'], int)]
        start_del = [v for v, cnt in collections.Counter(start_vals).items() if cnt > 1]

        end_vals = [self.solution_G.nodes[n]['value']
                    for n in self.solution_G.neighbors(self.end)
                    if isinstance(self.solution_G.nodes[n]['value'], int)]
        ec = collections.Counter(end_vals)
        end_del = [v for v, cnt in ec.items() if cnt > 1] if len(ec) > 1 else []

        gray_del = []
        for g in self.gray:
            gv = [self.solution_G.nodes[n]['value']
                  for n in self.solution_G.neighbors(g)
                  if isinstance(self.solution_G.nodes[n]['value'], int)]
            gray_del.extend(v for v, cnt in collections.Counter(gv).items() if cnt > 2)

        self.priority = [
            p for p in self.priority
            if not (p[0] in start_del or p[-1] in end_del or p[-1] in gray_del)
        ]
        return self.priority

    def select_a_move(self, node, priority):
        """Return all neighbors matching the next priority value (possibly multiple)."""
        avail = [
            nb for nb in self.solution_G.neighbors(node)
            if nb not in self.path
               and isinstance(self.solution_G.nodes[nb]['value'], int)
        ]
        order = list(priority[::-1] if node in self.gray else priority)
        for val in order:
            picks = [nb for nb in avail if self.solution_G.nodes[nb]['value'] == val]
            if picks:
                return picks
        return []

    def find_path(self):
        """
        Try each pruned priority until one yields a complete walk from start to end.
        Ties (>1) are now resolved deterministically by taking the first.
        """
        for pr in self.priority:
            self.path = [self.start]
            current = self.start

            while True:
                if current == self.end:
                    return self.path
                moves = self.select_a_move(current, pr)
                if not moves:
                    # dead end
                    break
                # previously: if len(moves)!=1: break
                # now pick the first in priority order
                current = moves[0]
                self.path.append(current)

        return []  # no valid path found

    def add_edge(self):
        for u, v in zip(self.path, self.path[1:]):
            self.solution_G.add_edge(u, v, path='path')

    def draw(self):
        edges = [(u, v) for u, v, d in self.solution_G.edges(data=True)
                 if d.get('path') == 'path']
        draw_graph(self.solution_G, self.positions, self.start,
                   self.end, self.gray, "Path Found", highlight_edges=edges)


if __name__ == "__main__":
# # ======================= Test 1: Eazy =======================
#     input_board = {
#         'input_list': [[3, 2, 2],
#                        [3, 2, 1],
#                        [3, 3, 2]],
#         'start': (1, 0),
#         'end': (1, 2),
#         'gray': None
#     }
#     # Draw the initial board graph
#     # board = Board(input_board)
#     # board.parse_board()
#     # board.draw()
#
#     # Use PuzzleSolver to find a path and display the result graph with highlighted path
#     solver = PuzzleSolver(input_board)
#     solver.pruning_strategy()
#     path = solver.find_path()
#     solver.add_edge()
#     solver.draw()
#     print("Found path:", path)
#
# # ======================= Test 2: Medium =======================
#     input_board = {
#         'input_list': [[4, 3, 2, 1, 2],
#                        [5, 2, 4, 3, 3],
#                        [3, 1, 1, 5, 4],
#                        ['X', 2, 3, 4, 5],
#                        ['X', 3, 5, 2, 3]],
#         'start': (4, 1),
#         'end': (0, 3),
#         'gray': [(2, 2)]
#     }
#
#     # Draw the initial board graph
#     board = Board(input_board)
#     board.parse_board()
#     board.draw()
#
#     # Use PuzzleSolver to find a path and display the result graph with highlighted path
#     solver = PuzzleSolver(input_board)
#     solver.pruning_strategy()
#     path = solver.find_path()
#     solver.add_edge()
#     solver.draw()
#     print("Found path:", path)

# ======================= Test 3: Hard =======================
    input_board = {
        'input_list': [
            [4, 6, 5, 7, 1, 'X', 5],
            [4, 'X', 'X', 'X', 'X', 'X', 4],
            [3, 'X', 3, 6, 7, 5, 6],
            [1, 3, 1, 4, 2, 1, 7],
            [6, 6, 3, 6, 7, 3, 'X'],
            [2, 4, 1, 'X', 2, 1, 'X'],
            [5, 'X', 6, 3, 4, 'X', 2]
        ],
        'start': (0, 4),
        'end': (6, 6),
        'gray': [(0, 2), (3, 1), (4, 4)]
    }

    solver = PuzzleSolver(input_board)
    solver.pruning_strategy()
    path = solver.find_path()
    solver.add_edge()
    solver.draw()
    print("Found path:", path)
