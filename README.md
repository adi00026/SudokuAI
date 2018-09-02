# SudokuAI
A bot that solves any sudoku puzzle on https://www.websudoku.com/

## How it works

SudokuAI is a bot that can solve any sudoku puzzle on https://www.websudoku.com/

Written in Python, the bot uses Python's Imaging Library, PIL and pyautogui to scan the screen, determine the grid, solve the puzzle and fill in the squares in under 30 seconds.

It uses core artificial intelligence algorithms such as search and constraint propogation to solve the puzzle. The actual puzzle takes under a second to solve with scanning the screen and determining the grid taking approximately 18 seconds and filling in the squares with the solved puzzle taking another 10 seconds.

## Challenges

One of the biggest challenges I faced while making the bot was scanning the screen in a reasonable amount of time to determine the value of each square.

Here's a screenshot of a typical grid at https://www.websudoku.com/ :

   ![screenshot](https://github.com/adi00026/SudokuAI/blob/master/typical_grid.png)

Each square can have one of ten possible values: a blank square or the digits 1-9.

Each individual square 31 units wide, while the entire grid 281 units wide. Were I to scan the entire grid, I would've had the RGBA values for almost 79,000 individual pixels. To scan and subsequently process this many RBG values would've taken an unreasonable amount of time (almost 5 hours) and wouldn't have been a viable solution to the problem I was trying to solve. I decided to be creative in my approach and calculated a way to determine the value of each square using only 2 RGB pixel values. I realized that I could use the 225th and 324th pixel of each square to determine its value. Hence, I was able to reduce the problem of scanning 79,000 pixels down to 162 pixels, 2 for each of the 81 squares.

## How I solved the grid

Anyone who has solved a Sudoku puzzle before knows that the easiest way to solve one is to use a process of elimination to find each square's value. Each square is part of a row, column and a collection of nine squares. In simpler puzzles, you can use the values of the other squares in the same row, column or collection to determine a square's value. Peter Norvig summarizes this algorithm in two lines: 

 >(1) If a square has only one possible value, then eliminate that value from the square's peers. 
 >(2) If a unit has only one possible place for a value, then put the value there.

This works fine for simpler puzzles, but not for harder ones. For harder puzzles, this method works up to a point. After that you have to guess a solution for a square and keep working until either:

1) You arrive at a contradiction in your grid and your guess was wrong
2) Your guess works and you either solve the puzzle or get to the point where you must guess again

My bot first tries solving the puzzle using the first method. This is called *constraint propogation.* We're reducing the domain of each square, and *propogating* that information to other squares in the grid. 

www.websudoku.com has 4 levels:
   ![screenshot](https://github.com/adi00026/SudokuAI/blob/master/levels.png)

Most easy and medium puzzles can be solved by constraint propogation.

Hard and evil puzzles however, require you to guess a solution for a square and work from there. This is called *search.* We're *searching* for a solution by systematically guessing when we must and evaluating game states to ensure there isn't a contradiction. I use a recursive search method in my bot to do this.

I've done my best to make my code easy to follow along. I've commented what each function and variable is used for. Feel free to have a look!

## Acknowledgements

