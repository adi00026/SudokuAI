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



## Acknowledgements

