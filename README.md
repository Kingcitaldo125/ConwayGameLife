# ConwayGameLife
[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python and Pygame.
This is essentially a [cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton), and Conway's Game of Life is also known as a 'Zero player game'.

## The Game Rules
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

## Usage

Simply invoke the script with a floating point argument telling the game how quickly to go.
The argument is a wait time, in seconds.
More below.
To quit the game, hit the `ESC` key.

### Linux
``` bash
# Wait for 1 second before processing the next frame
python3 main.py 1
```
### Windows
``` bash
# Wait for 1 second before processing the next frame
python main.py 1
```
