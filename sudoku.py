##################################################################### SudokuAI #####################################################################

'''
Bot that solves any sudoku puzzle on https://www.websudoku.com/ 
Also accepts a string representation of the puzzle or a text file as input.
'''

from PIL import ImageGrab
import time
import pyautogui
import sys

####################### Data used by GUI version #######################
# Maps the position of each quadrant on the screen.
posDict = {1: (635,305), 2: (735,305), 3: (835, 305), 4: (635, 405), 5: (735, 405), 6: (835, 405), 7: (635, 505), 8: (735, 505), 9: (835, 505)}

# Represents width of each square on the screen.
width = 33

# Each index in the list corresponds to the RGB pixel value of the number it represents.
RGBList = [[(255, 255, 255, 255), (255, 255, 255, 255)],[(255, 251, 214, 255), (156, 211, 247, 255)], [(255, 255, 255, 255), (49, 138, 189, 255)], [(239, 215, 189, 255), (239, 207, 165, 255)], [(165, 215, 247, 255), (0, 0, 0, 255)], [(165, 146, 123, 255), (255, 255, 231, 255)], [(0, 0, 0, 255), (255, 255, 255, 255)], [(255, 255, 255, 255), (0, 0, 82, 255)], [(0, 0, 0, 255), (0, 0, 0, 255)], [(255, 255, 255, 255), (49, 48, 0, 255)]]
solvedList = []

####################### Data used by both versions of the bot #######################
letters = "ABCDEFGHI"
numbers = "123456789"
sudoku = {}
numList = []
squares = []
allUnits = []
units = {}
peers = {}

'''
Sets up squares, allUnits, units and peers - the different data structures needed by the bot.
'''
def setUp():

	# Initializes squares
	global squares
	squares = [i + j for i in letters for j in numbers]	

	
	# Initializes allUnits
	global allUnits
	for x in letters:
		allUnits.append([x + y for y in numbers])

	for x in numbers:
		allUnits.append([y + x for y in letters])

	for x in ['ABC', 'DEF', 'GHI']:
		for y in ['123', '456', '789']:
			allUnits.append([i + j for i in x for j in y])

	
	# Initializes units
	global units
	for x in squares:
		units[x] = [y for y in allUnits if x in y]
	
	# Initializes peers
	global peers
	for x in squares:
		tempList = []
		newList = units[x]
		for a in newList:
				for y in a:
					if y not in tempList:
						tempList.append(y)
		tempList.remove(x)
		peers[x] = tempList
 
####################### Functions used by text version #######################
'''
Converts a string to a dictionary that represents the game state.
'''
def convert(seq):
    chars = [c for c in seq if c in numbers or c in '0.']
    global sudoku
    sudoku = dict(zip(squares, chars))
    for x,y in sudoku.items():
    	if y == '.':
    		sudoku[x] = '123456789'

'''
Prints answer in grid format.
'''
def arrange(game):
	print ""
	print "##########"
	print ""
	for letter in letters:
		line = ''
		for number in numbers:
			line = line + game[letter + number]
		print line

	print ""
	print "##########"

####################### Functions used by GUI version #######################
'''
Iterates over the different grid indices.
'''
def getNumbers():
	for w in range(0, 3):
		for x in range(0, 3):
			for y in range(0, 3):
				for z in range(0, 3):
					trial((posDict[w * 3 + 1 + y][0] + z * width, posDict[w * 3 + 1 + y][1] + x * width))

'''
Updates newList with the number in a square. Uses two pixels in a square to process the image and determine the number represented.
'''
def trial(pos):
	numList.append(RGBList.index([ImageGrab.grab().load()[pos[0] + 15, pos[1] + 15], ImageGrab.grab().load()[pos[0] + 18, pos[1] + 18]]))

'''
Converts newList to a grid such that each number corresponds to its square 'A1', 'A2',......,'I7', 'I8', 'I9'.
'''
def makeGrid():
	count = 0
	for x in letters:
		for y in numbers:
			if numList[count] == 0:
				sudoku[x + y] = '123456789'
			else:
				solvedList.append(x + y)
				sudoku[x + y] = str(numList[count])
			count += 1

'''
Part of bot; fills in answers on https://www.websudoku.com/ screen.
'''
def fillIn(game):
	print("Filling grid in now!")
	count = 0
	for w in range(0, 3):
		for x in range(0, 3):
			for y in range(0, 3):
				for z in range(0, 3):
					if squares[count] not in solvedList:
						pyautogui.click((posDict[w * 3 + 1 + y][0] + z * width + 16.5, posDict[w * 3 + 1 + y][1] + x * width + 16.5))
						pyautogui.press(game[squares[count]])
					count += 1
	
####################### Functions used by both versions of the bot #######################
'''
Prints how many squares have been solved.
'''
def solved(game):
	return len([x for x in squares if len(game[x]) == 1])

'''
Checks if configuration is legal according to the rules of sudoku.
'''
def legal(gameState):
	if gameState == False: return False

	for x in squares:
		for peer in peers[x]:
			if len(gameState[peer]) == 1 and len(gameState[x]) == 1 and gameState[peer] == gameState[x]:
				return False
		if len(gameState[x]) == 0:
			return False
	return True

'''
Eliminates numbers from peers.
'''
def eliminate(game):
	for x in squares:
		if len(game[x]) == 1:
			peerList = peers[x]
			for y in peerList:
				if game[x] in game[y]:
					game[y] = game[y].replace(game[x], '')

	for x in squares:
		unitList = units[x]
		for u in unitList:
			for digit in numbers:
				newList = [pos for pos in u if digit in game[pos]]
				if len(newList) == 1:
					game[newList[0]] = digit

	return (solved(game), game)

'''
When no more squares can be eliminated, it assumes a number for a sqaure and recursively continues.
If it hits upon an illegal game state, it backtracks.
'''
def search(game):

	if not legal(game): return False

	if solved(game) == 81: return game

	num = 9
	for s in squares:
		if len(game[s]) > 1:
			if len(game[s]) < num:
				num,square = len(game[s]), s   
	
	for digit in game[square]:
		attempt = game.copy()
		attempt[square] = digit
		answer = search(runner(attempt))
		if answer: return answer

'''
Executes eliminate until no more squares can be solved.
'''
def runner(game):
	num, game = eliminate(game)

	while True and legal(game):
		num2, game = eliminate(game)

		if num == num2 or num2 == 81:
			break
		else:
			num = num2

	return game

if __name__ == '__main__':

	start_time = time.time()

	setUp()

	cmdline = sys.argv
	
	if len(cmdline) == 1:
		time.sleep(2)
		print "Reading the screen....."
		getNumbers()
		makeGrid()
		print "Time taken to read screen: --- %s seconds --- " % (time.time() - start_time - 2)
		
	elif len(cmdline) == 2 and type(cmdline[1]) == str:
		convert(cmdline[1])
	
	elif len(cmdline) == 3 and cmdline[1] == '-f' and cmdline[2].rstrip('').endswith('.txt'):
		convert(file(cmdline[2]).read().strip())
	
	else:
		print "Please see read-me for usage"
		sys.exit()

	gui_start_time = time.time()
	
	runner(sudoku)

	# For GUI version
	if len(cmdline) == 1:
		if solved(sudoku) == 81:
			fillIn(sudoku)
			pyautogui.goto(660,660)
		else:
			fillIn(search(sudoku))

	# For string version
	else:
		arrange(search(sudoku))

	print(" ")
	print("Total Time: --- %s seconds ---" % (time.time() - start_time - 2))
	print(" ")
	