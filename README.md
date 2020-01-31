# Halma
### Implements Halma Agent in Halma.py 
### Actual game plays in the Notebook file.
<p align="center">
  <img width="300" height="300" src="https://github.com/wonhyukjang/Halma/blob/master/Halma.png">
</p>

Project description

In this project, we will play the game of Halma, an adversarial game with some similarities to
checkers. The game uses a 16x16 checkered gameboard. Each player starts with 19 game pieces
clustered in diagonally opposite corners of the board. To win the game, a player needs to
transfer all of their pieces from their starting corner to the opposite corner, into the positions
that were initially occupied by the opponent. 

In more details (from https://en.wikipedia.org/wiki/Halma):

Setup for two players:

- The board consists of a grid of 16 x 16 squares.
- Each player's camp consists of a cluster of adjacent squares in one corner of the board.
These camps are delineated on the board.
- For two-player games, each player's camp is a cluster of 19 squares. The camps are in
opposite corners.
- Each player has a set of pieces in a distinct color, of the same number as squares in each
camp.
- The game starts with each player's camp filled by pieces of their own color.

Play sequence:
We first describe the typical play for humans. 
- Create the initial board setup according to the above description.
- Players randomly determine who will move first.
- Pieces can move in eight possible directions (orthogonally and diagonally).
- Each player's turn consists of moving a single piece of one's own color in one of the
following plays:

<p align="center">
  <img width="600" height="400" src="https://github.com/wonhyukjang/Halma/blob/master/Moves.png">
</p>

We show examples of valid moves (in green) and invalid moves (in red). At left, the isolated
white piece can move to any of its empty 8 neighbors. At right, the central white piece can jump
over one adjacent piece if there is an empty cell on the other side. After one jump is executed,
possibly several other valid jumps can follow with the same piece and be combined in one move;
this is shown in the sequence of jumps that start with a down-right jump for the central piece.
Note that additional valid moves exist that are not shown (e.g., the central white piece could
move to some adjacent empty location).

Note the invalid moves: red arrow going left: cannot jump over one or more empty spaces plus
one or more pieces. Red arrow going left-down: cannot jump over one or more pieces plus one
or more empty spaces. Red arrow going down: cannot jump over more than one piece.
Playing with agents

Output: The file output.txt which your program creates in the current directory should be
formatted as follows:

1 or more lines: Describing your move(s). There are two possible types of moves (see above):

E FROM_X,FROM_Y TO_X,TO_Y – your agent moves one of your pieces from location
FROM_X, FROM_Y to adjacent empty location TO_X, TO_Y. We will again use zero-based,
horizontal-first, start at the top-left indexing in the board, as in homework 1. So, location
0,0 is the top-left corner of the board; location 15,0 of the top-right corner; location 0,15
is the bottom-left corner, and location 15,15 the bottom-right corner. As explained above,
TO_X,TO_Y should be adjacent to FROM_X,FROM_Y (8-connected) and should be empty.
If you make such a move, you can only make one per turn.

J FROM_X,FROM_Y TO_X,TO_Y – your agent moves one of your pieces from location
FROM_X,FROM_Y to empty location TO_X,TO_Y by jumping over a piece in between. You
can make several such jumps using the same piece, as explained above, and should write
out one jump per line in output.txt.


