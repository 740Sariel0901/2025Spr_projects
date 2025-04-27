import random
import matplotlib.pyplot as plt
import networkx as nx
import itertools
from matplotlib.style.core import available
from networkx.algorithms.threshold import threshold_graph

# board = [['X', 'X', 'X', 'X', 'X', 'X', 'X'],
#          ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
#          ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
#          ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
#          ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
#          ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
#          ['X', 'X', 'X', 'X', 'X', 'X', 'X']]
#
# priority = [7, 2, 3, 6, 4, 5, 1]
# path = [(0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 1), (3, 2), (2, 2), (2, 3), (3, 4), (4, 4), (5, 5), (6, 6)]
# start = (0, 4)
# end = (6, 6)
# gray = [(0, 2), (3, 1), (4, 4)]


# def build_graph(board, neighbor_dirs=None):
#     """
#     Build a NetworkX graph from a 2D board.
#
#     Args:
#       board: 2D list of values.
#       neighbor_dirs: List of (dr,dc) offsets for edges. Defaults to 6-directional.
#
#     Returns:
#       G: networkx.Graph with node attribute 'value'.
#       pos: dict mapping node -> (x, y) for plotting.
#     """
#     if neighbor_dirs is None:
#         neighbor_dirs = [(-1, 0), (0, 1), (1, 1), (1, 0), (0, -1), (-1, -1)]
#     G = nx.Graph()
#     pos = {}
#     rows = len(board)
#     cols = len(board[0]) if rows else 0
#
#     # Add nodes and positions
#     for r in range(rows):
#         for c in range(cols):
#             node = (r, c)
#             G.add_node(node, value=board[r][c])
#             pos[node] = (c - 0.5 * r, -r)
#
#     # Add edges based on neighbor directions
#     for r in range(rows):
#         for c in range(cols):
#             for dr, dc in neighbor_dirs:
#                 nr, nc = r + dr, c + dc
#                 if 0 <= nr < rows and 0 <= nc < cols:
#                     G.add_edge((r, c), (nr, nc))
#
#     return G, pos
#
#
#
# def draw_graph(G, positions, start, end, gray, path, title="Graph Visualization"):
#     """
#     Draw the graph highlighting start, end, gray, and path nodes and edges,
#     in the same style as draw_graph.
#
#     Parameters:
#     - G: The graph to be drawn.
#     - positions: A dictionary mapping nodes to (x, y) positions.
#     - start, end: The start and end nodes (colored red and green).
#     - gray: List of nodes to color gray.
#     - path: List of nodes defining the path to highlight in yellow, with edges in blue.
#     - title: Title for the plot.
#     """
#     plt.figure(figsize=(6, 6))
#
#     # Node labels: show node tuple and its 'value' attribute
#     labels = {node: f"{node}\n{G.nodes[node]['value']}" for node in G.nodes()}
#
#     # Assign colors
#     node_colors = []
#     for node in G.nodes():
#         if node == start:
#             node_colors.append("red")
#         elif node == end:
#             node_colors.append("green")
#         elif node in gray:
#             node_colors.append("gray")
#         elif node in path:
#             node_colors.append("yellow")
#         else:
#             node_colors.append("skyblue")
#
#     # Draw nodes and labels
#     nx.draw_networkx_nodes(G, pos=positions, node_color=node_colors, node_size=500)
#     nx.draw_networkx_labels(G, pos=positions, labels=labels, font_size=7)
#
#     # Prepare edge lists: path edges vs. normal edges
#     path_edges = list(zip(path[:-1], path[1:]))
#     highlight_set = set(path_edges)
#     normal_edges = [
#         e for e in G.edges()
#         if e not in highlight_set and (e[1], e[0]) not in highlight_set
#     ]
#
#     # Draw edges
#     nx.draw_networkx_edges(G, pos=positions, edgelist=normal_edges, edge_color="gray")
#     nx.draw_networkx_edges(
#         G, pos=positions, edgelist=path_edges,
#         edge_color="blue", width=3
#     )
#
#     plt.title(title)
#     plt.axis("off")
#     plt.show()


def assign_value(graph, priority, path, start, end, gray, n = 7):
    """
    This function selects primary nodes and assign adjacent priority pairs to nodes along a path
    so that movement priority is inferable.
    """
    # To establish a unique ordering among n items, we need at least n–1 pairwise comparisons.
    # For example, if 7 items are ordered 1 > 2 > 3 > 4 > 5 > 6 > 7,
    # we need the comparisons [1>2, 2>3, 3>4, 4>5, 5>6, 6>7] to reconstruct that exact sequence.
    k = n - 1

    # 1. Identify internal nodes (exclude start/end)
    internal_nodes = [i for i in path if i != end]
    # Map each internal node to its index in the path
    index_map = {node: idx for idx, node in enumerate(path)}

    # 2. Sample primary nodes and adjacent priority pairs
    candidate_primary_nodes = [node for node in internal_nodes if any(nb not in path for nb in graph.neighbors(node))]
    primary_nodes = random.sample(candidate_primary_nodes, k)
    # print(primary_nodes)
    priority_pairs = [(priority[i], priority[i + 1]) for i in range(k)]
    # print(priority_pairs)

    # 3. Assign values to primary nodes and their successors
    graph = assign_primary_value_pair(graph, path, priority, end, index_map, primary_nodes, priority_pairs, gray)

    # 4. Randomly assign values to remaining nodes on path
    graph = assign_value_to_remaining_nodes_on_path(graph, path, start, index_map, priority, gray)

    # 5. Keep the neighbor of end node "X" to ensure the "dead-end"

    # 6. Fill common external neighbors
    graph = assign_value_to_remaining_neighbors_of_on_path_nodes(graph, path, internal_nodes, end, gray, priority, index_map)

    # 7. Assign any remaining nodes a random value
    graph = assign_value_to_any_remaining_nodes(graph, path, priority)
    return graph


def assign_primary_value_pair(graph, path, priority, end, index_map, primary_nodes, priority_pairs, gray):
    # Store assigned priority pairs and nodes
    assigned = {}
    _ = 0
    attempts = 0
    max_attempts = 500

    while _ != len(primary_nodes):
        attempts += 1
        if attempts > max_attempts:
            raise ValueError(f"stuck assigning at node index {_}… giving up")

        node = primary_nodes[_]
        next_node = path[index_map[node] + 1]
        neighbor_values = [graph.nodes[n]['value'] for n in graph.neighbors(node)]
        numeric_values = [v for v in neighbor_values if isinstance(v, int)]
        unique_numeric_values = list(set(numeric_values))

        if node in gray:
            if len(unique_numeric_values) == 0:
                # Randomly pick a node to assign value
                picked_neighbor_node = random.choice([node for node in graph.neighbors(node)
                                                      if node not in path and node not in graph.neighbors(end)])
                # If the randomly picked node is also a neighbor of a node on the path,
                # its value cannot be the highest priority (lowest in the reverse priority)
                if set(graph.neighbors(picked_neighbor_node)) & set(path):
                    priority_pair = random.choice([priority_pair for priority_pair in priority_pairs
                                                   if (priority_pair not in assigned
                                                       and priority_pair != priority_pairs[0])])
                else:
                    # Randomly pick a priority pair
                    priority_pair = random.choice([priority_pair for priority_pair in priority_pairs
                                                   if priority_pair not in assigned])
                low_val, high_val = priority_pair
                graph.nodes[picked_neighbor_node]['value'], graph.nodes[next_node]['value'] = low_val, high_val
                # print("low: ", low_val, " high: ", high_val)
                # print('picked_neighbor_node: ', picked_neighbor_node, 'next_node: ', next_node, 'node: ', node)
                assigned[priority_pair] = {'node': node, 'next_node': next_node,
                                           'picked_neighbor_node': picked_neighbor_node}
                _ += 1
            else:
                # We need to ensure that next_node’s value is greater than the value of any neighbor of the current node.
                # Find the minimum priority value among the current node’s neighbors.
                top_priority = max(unique_numeric_values, key=lambda x: priority.index(x))
                # Get the matching index
                priority_pair_idx = next(i for i, (y, _) in enumerate(priority_pairs) if y == top_priority)
                # Assign next node with higher priority
                priority_pair_lst = [priority_pair for priority_pair in priority_pairs[priority_pair_idx:]
                                     if priority_pair not in assigned]
                if len(priority_pair_lst):
                    priority_pair = random.choice(priority_pair_lst)
                    low_val, high_val = priority_pair
                    if low_val == top_priority:
                        # Do not need bother to assign another node since we've already got enough clue
                        graph.nodes[next_node]['value'] = high_val
                        picked_neighbor_node = [n for n in graph.neighbors(node) if graph.nodes[n]['value'] == top_priority][0]
                    else:
                        # Randomly pick a node (without numeric value) to assign value
                        picked_neighbor_node = random.choice([node for node in graph.neighbors(node)
                                                              if graph.nodes[node]['value'] == "X"
                                                              and node not in path
                                                              and node not in graph.neighbors(end)])
                        graph.nodes[picked_neighbor_node]['value'], graph.nodes[next_node]['value'] = low_val, high_val
                    assigned[priority_pair] = {'node': node, 'next_node': next_node,
                                               'picked_neighbor_node': picked_neighbor_node}
                    # print("low: ", low_val, " high: ", high_val)
                    # print('picked_neighbor_node: ', picked_neighbor_node, 'next_node: ', next_node, 'node: ', node)
                    _ += 1
                else:
                    # No valid value pair found, the value of the current node's neighbor is too high.
                    # We need to reassign the previous value
                    assigned, _ = back_track(graph, top_priority, assigned, _)
                    continue
        else:
            if len(unique_numeric_values) == 0:
                # Randomly pick a node to assign value
                picked_neighbor_node = random.choice([node for node in graph.neighbors(node)
                                                      if node not in path and node not in graph.neighbors(end)])
                # If the randomly picked node connects a gray node that on the path,
                # it cannot have the lowest priority value
                if set(graph.neighbors(picked_neighbor_node)) & set((set(gray) & set(path))):
                    priority_pair = random.choice([priority_pair for priority_pair in priority_pairs
                                                   if (priority_pair not in assigned
                                                       and priority_pair != priority_pairs[-1])])
                else:
                    # Randomly pick a priority pair
                    priority_pair = random.choice([priority_pair for priority_pair in priority_pairs
                                                   if priority_pair not in assigned])
                high_val, low_val = priority_pair
                graph.nodes[picked_neighbor_node]['value'], graph.nodes[next_node]['value'] = low_val, high_val
                assigned[priority_pair] = {'node': node, 'next_node': next_node, 'picked_neighbor_node': picked_neighbor_node}
                # print("low: ", low_val, " high: ", high_val)
                # print('picked_neighbor_node: ', picked_neighbor_node, 'next_node: ', next_node, 'node: ', node)
                _ += 1
            else:
                # We need to ensure that next_node’s value is greater than the value of any neighbor of the current node.
                # Find the maximum priority value among the current node’s neighbors.
                top_priority = min(unique_numeric_values, key=lambda x: priority.index(x))
                # Get the matching index
                priority_pair_idx = next(i for i, (_, y) in enumerate(priority_pairs) if y == top_priority)
                # Assign next node with higher priority
                priority_pair_lst = [priority_pair for priority_pair in priority_pairs[:priority_pair_idx + 1]
                                               if priority_pair not in assigned]
                if len(priority_pair_lst):
                    priority_pair = random.choice(priority_pair_lst)
                    high_val, low_val = priority_pair
                    if low_val == top_priority:
                        # Do not need bother to assign another node since we've already got enough clue
                        graph.nodes[next_node]['value'] = high_val
                        picked_neighbor_node = [n for n in graph.neighbors(node) if graph.nodes[n]['value'] == top_priority][0]
                    else:
                        # Randomly pick a node (without numeric value) to assign value
                        picked_neighbor_node = random.choice([node for node in graph.neighbors(node)
                                                              if graph.nodes[node]['value'] == "X"
                                                              and node not in path
                                                              and node not in graph.neighbors(end)])
                        graph.nodes[picked_neighbor_node]['value'], graph.nodes[next_node]['value'] = low_val, high_val
                    assigned[priority_pair] = {'node': node, 'next_node': next_node, 'picked_neighbor_node': picked_neighbor_node}
                    # print("low: ", low_val, " high: ", high_val)
                    # print('picked_neighbor_node: ', picked_neighbor_node, 'next_node: ', next_node, 'node: ', node)
                    _ += 1
                else:
                    # No valid value pair found, the value of the current node's neighbor is too high.
                    # We need to reassign the previous value
                    assigned, _ = back_track(graph, top_priority, assigned, _)
                    continue
    return graph



def back_track(graph, top_priority, assigned, _):
    """This function make top_priority lower and the priority of related nex node value lower"""
    # Find the corresponding value pair
    problem_value_pair = next(k for k in assigned.keys() if k[1] == top_priority)

    # Turn value to "X"
    start = False
    count = 0
    for key in list(assigned.keys()):
        if key == problem_value_pair:
            start = True
            picked_neighbor_node = assigned[key]['picked_neighbor_node']
            graph.nodes[picked_neighbor_node]['value'] = "X"
            next_node = assigned[key]['next_node']
            graph.nodes[next_node]['value'] = "X"
            del assigned[key]
        if not start:
            count += 1
            continue
    _ = count
    return assigned, _


def assign_value_to_remaining_nodes_on_path(graph, path, start, index_map, priority, gray):
    """This function assign value to remaining nodes on path"""
    # Loop through the nodes on path
    for node in path:
        if node == start:   # The first node can have any value
            graph.nodes[node]['value'] = random.choice(priority + ["X"] )
            continue
        # Check if the node has a value (skip the nodes that already has a value)
        if graph.nodes[node]['value'] != "X":
            continue
        last_node = path[index_map[node] - 1]

        if last_node in gray:
            # Get the min of the last node neighbor's value (make sure this node is the best and only choice for last node)
            neighbor_values = [graph.nodes[n]['value'] for n in graph.neighbors(last_node)]
            numeric_values = [v for v in neighbor_values if isinstance(v, int)]
            unique_numeric_values = list(set(numeric_values))
            top_priority = max(unique_numeric_values, key=lambda x: priority.index(x))
            priority_idx = priority.index(top_priority)
            priority_lst = priority[priority_idx + 1:]
            # Randomly assign a value (higher than the baseline)
            graph.nodes[node]['value'] = random.choice(priority_lst)
        else:
            # Get the max of the last node neighbor's value (make sure this node is the best and only choice for last node)
            neighbor_values = [graph.nodes[n]['value'] for n in graph.neighbors(last_node)]
            numeric_values = [v for v in neighbor_values if isinstance(v, int)]
            unique_numeric_values = list(set(numeric_values))
            top_priority = min(unique_numeric_values, key=lambda x: priority.index(x))
            priority_idx = priority.index(top_priority)
            priority_lst = priority[:priority_idx]
            # Randomly assign a value (higher than the baseline)
            graph.nodes[node]['value'] = random.choice(priority_lst)
    return graph


def assign_value_to_remaining_neighbors_of_on_path_nodes(graph, path, internal_nodes, end, gray, priority, index_map):
    for node in internal_nodes:
        neighbors = [nb for nb in graph.neighbors(node) if nb not in graph.neighbors(end) and graph.nodes[nb]['value'] == "X"]
        next_node = path[index_map[node] + 1]
        next_node_value_idx = priority.index(graph.nodes[next_node]['value'])
        if node not in gray:
            # must pick from the “higher” half
            available_value = priority[next_node_value_idx + 1:]
        else:
            # must pick from the “lower” half
            available_value = priority[:next_node_value_idx]

        if not available_value:
            continue  # nothing to assign here

            # assign a random choice to every neighbor
        for nb in neighbors:
            graph.nodes[nb]['value'] = random.choice(available_value)
    return graph


def assign_value_to_any_remaining_nodes(graph, path, priority):
    all_neighbors = []
    for node in path:
        all_neighbors.append(graph.neighbors(node))
    all_neighbors = list(itertools.chain.from_iterable(all_neighbors))
    remaining_nodes = [node for node in graph.nodes if node not in all_neighbors]
    for node in remaining_nodes:
        graph.nodes[node]['value'] = random.choice(priority)
    return graph


# if __name__ == "__main__":
#     import time
#
#     while True:
#         # rebuild from scratch
#         G, pos = build_graph(board, neighbor_dirs=None)
#
#         try:
#             G = assign_value(G, priority, path, start, end, gray, n=7)
#         except (StopIteration, ValueError, IndexError) as e:
#             print(f"[retry] assignment failed ({e!r}), retrying…")
#             time.sleep(0.1)
#             continue
#         else:
#             break
#     draw_graph(G, pos, start, end, gray, path)







