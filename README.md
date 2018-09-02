# SudokuAI
A bot that solves any sudoku puzzle on https://www.websudoku.com/

# How it works

SudokuAI is a bot that can solve any sudoku puzzle on https://www.websudoku.com/

Written in Python, the bot uses Python's Imaging Library, PIL and pyautogui to scan the screen, determine the grid, solve the puzzle
and fill in the squares in under 30 seconds.

It uses core artificial intelligence algorithms such as search and constraint propogation to solve the puzzle. The actual puzzle takes under
a second to solve with scanning the screen and determining the grid taking approximately 18 seconds and filling in the squares with the solved puzzle taking another 10 seconds.

# Challenges

One of the biggest challenges I faced while making the bot was scanning the screen in a reasonable amount of time. 

Here's a screenshot of a typical grid at https://www.websudoku.com/ :

   ![screenshot](https://github.com/adi00026/SudokuAI/blob/master/typical_grid.png)

Each individual square 31 units wide, while the entire grid 281 units wide. Were I to scan the entire grid, I would've had the RGBA values for almost 79,000 individual pixels. To scan and subsequently process this many RBG values would've taken an unreasonable amount of time and wouldn't have been a viable solution to the problem I was trying to solve. 

## Acknowledgements

