# 2025 Spring Final Projects - Yuran Zhang

## Game Rules:
Board: The board is a diamond shape. Every node is hexagon and contain a number inside. The size of the board can be difined by the player.
Priority: The numbers on the board are totally ordered, meaning there is exactly one way to compare their magnitudes.
Move: Can only move to a neighbor node with a higher priority. Stop move when meet a "dead-end". 
Dead-End: If a node can move to more than two neighbor node, it is called "dead-end", means cannot move forward in this case.
End: The end point must be a dead-end. Cannot move beyond the end point.
Gray: When steping into a gray node, the priority will reverse.
X: Cannot step on nodes contain "X" inside.
Task: Player need to find the only one path (move from start


## How Solver Work:
![image](https://github.com/user-attachments/assets/c1724215-86fd-4025-a527-bb1c114ffb57)


(Making original _variations_ of puzzles and games isn't as difficult as it may seem -- we have already done this in class. _Though admittedly, making *good* game variations -- that are well-balanced, strategically interesting, with good replay value_ can take expertise or luck and play-testing with revisions.  Such balanced elegance is desirable but might not be achievable here, given the short time you have.)

1. Devise your own new _original_ type of logic puzzle or an _original variation_ of existing puzzle type. Like with previous homework, your program should be able to randomly generate new puzzles of your type and automatically verify that all puzzles generated comply with the standard meta-rule that only one valid solution exists. It needs to output the _unsolved_ puzzles in a way that a human can print or view them conveniently to try solving them and to somehow output (to file?) or display the solution for each puzzle when requested, so as not to spoil the challenge. An interactive UI to "play" the puzzles interactively is very nice but *not* required. 

2. OR develop an AI game player for an _original variation_ of some existing strategy game.  If you do this, it needs to be set up so it can either play computer-vs-computer and/or against human players with a reasonable text or graphical UI. 2B. If two teams want to independently develop AI players for the same type of game variant as each other (but using different algorithms, strategies, and/or data structures) so they can compete, that is okay.  A sub-variation is to enable this game type on our course game server, discuss with the instructor if this is of interest.


## How Generator Work:

* Have some fun!
* In your own fork, please replace this README.md file's contents with a good introduction to your own project. 
* Targeted Algorithm Analysis:  Regardless of which option you choose, you need to _describe the performance characteristics of some critical parts of your program and explain why you chose the data structures and core algorithm(s) you did_. Examples, if you chose Type #1, what's the Big-O, Big-Theta, or Big-Omega run-time complexity of your puzzle solver? Or the puzzle generator? If you're doing Type #2 and using minimax or negamax, what's the complexity of your _heuristic evaluation function_? ...and of the function that finds all legal moves from a game state? 
* Performance Measurement: Supplement the analysis above with run-time measurements of multiple iterations of the game or puzzles as discussed in class. Sample results from a run-time profiler is a good idea at least as part of the measurements.
* If your team has more than one student, we expect everyone to make substantial git commits, with all members working on the programming. In addition, your README documentation should include a summary of how you shared the work.
* Live in-class presentation & demonstration of your work.
