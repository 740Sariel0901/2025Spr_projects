# 2025 Spring Final Projects - Yuran Zhang (yuranz5)

## Game Rules

- **Board**  
  A diamond-shaped grid of hexagonal cells, each containing a number. The player chooses the board’s size.

- **Priority Order**  
  All numbers are totally ordered—there is exactly one way to compare any two.

- **Path**  
  A sequence of adjacent moves from the start edge to the opposite edge.
  
- **Move**  
  You may only move to an adjacent cell whose number has strictly higher priority. Movement stops at a dead end.

- **Dead End**  
  Any cell that has more than two available higher-priority neighbors is considered a dead end—you cannot move forward from it.

- **End Point**  
  The designated end must itself be a dead end. You cannot move beyond it.

- **Gray Cells**  
  Entering a gray cell reverses the priority order for all subsequent moves.

- **Blocked Cells**  
  Cells marked with “X” cannot be entered.

- **Objective**  
  Find the unique valid path from the start to the end cell, and determine the priority sequence that makes it work.

---

## How the Solver Works

![Solver Workflow](https://github.com/user-attachments/assets/477cb020-c976-4bd5-a769-7e4e834a32f2)

A brute-force approach，The puzzle and solution will be stored in agraph data structure. Each cell is a node and the number are the values of them.

1. **Generate All Priority Permutations**  
   List every possible ordering of the board’s numbers.

2. **Prune Impossible Sequences**  
   - **Start Neighbors**: If more than two neighbors around the start share the same value, that value cannot come first in the priority sequence (it must rank below the other start-adjacent values).  
   - **End & Gray Neighbors**: If more than two neighbors around the end or any gray cell share the same value, that value cannot come last in the sequence (it must rank above the other surrounding values).

3. **Simulate Movement**  
   For each remaining priority sequence, step through the board: at each cell, move to the one neighbor whose value matches the next priority. Stop when you reach the end or hit a dead end.

4. **Select the Unique Path**  
   Identify which priority sequence yields exactly one valid path from start to end. Return that path and its corresponding priority order.
5. Visulization
   Highlight the edge connects the nodes when find the path.

---

## How Generator Work:
![image](https://github.com/user-attachments/assets/c1724215-86fd-4025-a527-bb1c114ffb57)

1. **Board Construction (Path_and_Gray):**
   - Builds an n×n grid, projects hex coordinates into 2D for plotting.
   - Chooses random start/end nodes on opposite edges.
   - Randomly selects ⌊n/2⌋ gray cells along the eventual path.

2. **Path Generation:**
   - Depth-first search with backtracking to find any path that has at least n–1 “branchable” nodes (each with at least one off-path neighbor).

3. **Value Assignment (assign_value):**
   - Iteratively assigns “comparison clues” (priority pairs) to on-path neighbors.
   - Uses back_track() to undo conflicting assignments.
   - Ensures all off-path neighbors of on-path nodes become “X” where necessary to block alternate routes.

4. **Validation:**
   - After assignment, re-run the brute-force solver to confirm exactly one valid path remains.
   - If not, repeat assignment from scratch.

5. **Visualization (draw_graph):**
   - Colors start/end/gray/X and highlights the unique path with colored nodes and edges.

