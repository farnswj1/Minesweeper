'''
Justin Farnsworth
Minesweeper Grid
February 12, 2020

'''

# Imported modules
import pygame
from random import randint
from time import time
from box import Box
from config import *


# Grid class
class Grid(object):
    # Constructor
    def __init__(self, width, height, boxSize, numberOfMines, x = 0, y = 0):
        self.__boxes = []
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__boxSize = boxSize
        self.__numberOfMines = numberOfMines
        self.__boxValueFont = pygame.font.SysFont('arial', boxSize)
        self.__numberOfFlagsLeft = str(numberOfMines)
        self.__numberOfSafeBoxes = (width * height) - numberOfMines
        self.__clickEnabled = True
        self.__firstClick = True
        self.__clickedAllSafeBoxes = False
        self.__clickedOnMine = False
        self.__gameOver = False
        self.__startTime = None
        self.__endTime = None

        # Intializes the boxes for the grid.
        for y in range(self.__y, self.__y + self.__height * self.__boxSize, self.__boxSize):
            row = []
            for x in range(self.__x, self.__x + self.__width * self.__boxSize, self.__boxSize):
                row.append(Box(x, y, self.__boxSize))
            self.__boxes.append(row)


    # Private functions


    # Randomly places a specified number of mines on the grid.
    # The clicked box and its adjacent boxes are excluded from being a potential mine.
    def __deployMines(self, box):
        # Calculates the index of the box
        boxIndexOnGridX = (box.getX() - self.__x) // self.__boxSize
        boxIndexOnGridY = (box.getY() - self.__y) // self.__boxSize

        # Deploys the mines.
        for i in range(self.__numberOfMines):
            mineDeployed = False
            
            # Loop repeats until a mine has its own coordinates.
            while not mineDeployed:
                x = randint(0, self.__width - 1)
                y = randint(0, self.__height - 1)

                # Checks if box[y][x] is adjacent to the clicked box. 
                # If so, then x and y are randomly generated again.
                if not boxIndexOnGridX - 1 <= x <= boxIndexOnGridX + 1 or not boxIndexOnGridY - 1 <= y <= boxIndexOnGridY + 1:
                    # Saves the value of the box as a mine if current box isn't already one.
                    # The while loop is also terminated when the mine has been deployed.
                    if self.__boxes[y][x].getValue() != 'X':
                        self.__boxes[y][x].updateValue('X')
                        mineDeployed = True
        
        # All boxes count the number of adjacent mines and their respective values are saved.
        for y in range(self.__height):
            for x in range(self.__width):
                # If the current box is a mine, then the counting is skipped for this box.
                if self.__boxes[y][x].getValue() != 'X':
                    adjacentMines = 0

                    # Interior boxes
                    if 0 < x < self.__width - 1 and 0 < y < self.__height - 1:
                        if self.__boxes[y - 1][x].getValue() == 'X': adjacentMines += 1     # Box directly above
                        if self.__boxes[y + 1][x].getValue() == 'X': adjacentMines += 1     # Box directly below
                        if self.__boxes[y][x - 1].getValue() == 'X': adjacentMines += 1     # Box to the left
                        if self.__boxes[y][x + 1].getValue() == 'X': adjacentMines += 1     # Box to the right
                        if self.__boxes[y - 1][x - 1].getValue() == 'X': adjacentMines += 1 # Box to the top-left
                        if self.__boxes[y - 1][x + 1].getValue() == 'X': adjacentMines += 1 # Box to the top-right
                        if self.__boxes[y + 1][x - 1].getValue() == 'X': adjacentMines += 1 # Box to the bottom-left
                        if self.__boxes[y + 1][x + 1].getValue() == 'X': adjacentMines += 1 # Box to the bottom-right
                    
                    # Left-most column (excluding corners)
                    elif x == 0 and 0 < y < self.__height - 1:
                        if self.__boxes[y - 1][0].getValue() == 'X': adjacentMines += 1 # Box directly above
                        if self.__boxes[y + 1][0].getValue() == 'X': adjacentMines += 1 # Box directly below
                        if self.__boxes[y - 1][1].getValue() == 'X': adjacentMines += 1 # Box to the top-right
                        if self.__boxes[y + 1][1].getValue() == 'X': adjacentMines += 1 # Box to the bottom-right
                        if self.__boxes[y][1].getValue() == 'X': adjacentMines += 1     # Box to the right

                    # Right-most column (excluding corners)
                    elif x == self.__width - 1 and 0 < y < self.__height - 1:
                        if self.__boxes[y - 1][-1].getValue() == 'X': adjacentMines += 1 # Box directly above
                        if self.__boxes[y + 1][-1].getValue() == 'X': adjacentMines += 1 # Box directly below
                        if self.__boxes[y - 1][-2].getValue() == 'X': adjacentMines += 1 # Box to the top-left
                        if self.__boxes[y + 1][-2].getValue() == 'X': adjacentMines += 1 # Box to the bottom-left
                        if self.__boxes[y][-2].getValue() == 'X': adjacentMines += 1     # Box to the left

                    # Top row (excluding corners)
                    elif 0 < x < self.__width - 1 and y == 0:
                        if self.__boxes[0][x - 1].getValue() == 'X': adjacentMines += 1 # Box to the left
                        if self.__boxes[0][x + 1].getValue() == 'X': adjacentMines += 1 # Box to the right
                        if self.__boxes[1][x - 1].getValue() == 'X': adjacentMines += 1 # Box to the bottom-left
                        if self.__boxes[1][x + 1].getValue() == 'X': adjacentMines += 1 # Box to the bottom-right
                        if self.__boxes[1][x].getValue() == 'X': adjacentMines += 1     # Box directly below

                    # Bottom row (excluding corners)
                    elif 0 < x < self.__width - 1 and y == self.__height - 1:
                        if self.__boxes[-1][x - 1].getValue() == 'X': adjacentMines += 1 # Box to the left
                        if self.__boxes[-1][x + 1].getValue() == 'X': adjacentMines += 1 # Box to the right
                        if self.__boxes[-2][x - 1].getValue() == 'X': adjacentMines += 1 # Box to the top-left
                        if self.__boxes[-2][x + 1].getValue() == 'X': adjacentMines += 1 # Box to the top-right
                        if self.__boxes[-2][x].getValue() == 'X': adjacentMines += 1     # Box directly above

                    # Top-left corner
                    elif x == 0 and y == 0:
                        if self.__boxes[0][1].getValue() == 'X': adjacentMines += 1 # Box to the right
                        if self.__boxes[1][0].getValue() == 'X': adjacentMines += 1 # Box directly below
                        if self.__boxes[1][1].getValue() == 'X': adjacentMines += 1 # Box to the bottom-right

                    # Top-right corner
                    elif x == 0 and y == self.__height - 1:
                        if self.__boxes[-1][1].getValue() == 'X': adjacentMines += 1 # Box to the right
                        if self.__boxes[-2][0].getValue() == 'X': adjacentMines += 1 # Box directly above
                        if self.__boxes[-2][1].getValue() == 'X': adjacentMines += 1 # Box to the top-right

                    # Bottom-left corner
                    elif x == self.__width - 1 and y == 0:
                        if self.__boxes[0][-2].getValue() == 'X': adjacentMines += 1 # Box to the left
                        if self.__boxes[1][-1].getValue() == 'X': adjacentMines += 1 # Box directly below
                        if self.__boxes[1][-2].getValue() == 'X': adjacentMines += 1 # Box to the bottom-left

                    # Bottom-right corner
                    elif x == self.__width - 1 and y == self.__height - 1:
                        if self.__boxes[-1][-2].getValue() == 'X': adjacentMines += 1 # Box to the left
                        if self.__boxes[-2][-1].getValue() == 'X': adjacentMines += 1 # Box directly above
                        if self.__boxes[-2][-2].getValue() == 'X': adjacentMines += 1 # Box to the top-left
                    
                    # Updates the value of the box by saving the number of adjacent mines.
                    self.__boxes[y][x].updateValue(adjacentMines)


    # Iteratively shows the values of the boxes.
    # If the box has no value, then the adjacent boxes are also flipped.
    # Base case is when the value of the box is 'X' or not 0.
    def __flipBox(self, clickedBox):
        # Creates a list of boxes that will be flipped. The clicked box is inserted initially.
        boxesToBeFlipped = [clickedBox]
        clickedBox.clickBox()

        # The loop repeats until the list is empty.
        while len(boxesToBeFlipped) > 0:
            box = boxesToBeFlipped[0]
            
            # If the box isn't a mine, then the number of safe boxes remaining decreases by 1.
            if box.getValue() != 'X':
                self.__numberOfSafeBoxes -= 1

            # If the clicked box was flagged, then the number of flags left increases by 1.
            # The flag is also flipped. (set to False)
            if box.isFlagged():
                box.flipFlag()
                self.__numberOfFlagsLeft = str(int(self.__numberOfFlagsLeft) + 1)

            # If the box's value is 0, then the adjacent boxes are added if not clicked already.
            if box.getValue() == '0':
                x, y = (box.getX() - self.__x) // self.__boxSize, (box.getY() - self.__y) // self.__boxSize

                # Interior boxes
                if 0 < x < self.__width - 1 and 0 < y < self.__height - 1:
                    # Box directly above
                    if not self.__boxes[y - 1][x].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y - 1][x])
                        self.__boxes[y - 1][x].clickBox()

                    # Box directly below
                    if not self.__boxes[y + 1][x].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y + 1][x])
                        self.__boxes[y + 1][x].clickBox()

                    # Box to the left
                    if not self.__boxes[y][x - 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y][x - 1])
                        self.__boxes[y][x - 1].clickBox()

                    # Box to the right
                    if not self.__boxes[y][x + 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y][x + 1])
                        self.__boxes[y][x + 1].clickBox()

                    # Box to the top-left
                    if not self.__boxes[y - 1][x - 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y - 1][x - 1])
                        self.__boxes[y - 1][x - 1].clickBox()

                    # Box to the top-right
                    if not self.__boxes[y - 1][x + 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y - 1][x + 1])
                        self.__boxes[y - 1][x + 1].clickBox()

                    # Box to the bottom-left
                    if not self.__boxes[y + 1][x - 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y + 1][x - 1])
                        self.__boxes[y + 1][x - 1].clickBox()

                    # Box to the bottom-right
                    if not self.__boxes[y + 1][x + 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y + 1][x + 1])
                        self.__boxes[y + 1][x + 1].clickBox()

                # Left-most column (excluding corners)
                elif x == 0 and 0 < y < self.__height - 1:
                    # Box directly above
                    if not self.__boxes[y - 1][0].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y - 1][0])
                        self.__boxes[y - 1][0].clickBox()

                    # Box directly below
                    if not self.__boxes[y + 1][0].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y + 1][0])
                        self.__boxes[y + 1][0].clickBox()

                    # Box to the top-right
                    if not self.__boxes[y - 1][1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y - 1][1])
                        self.__boxes[y - 1][1].clickBox()

                    # Box to the bottom-right
                    if not self.__boxes[y + 1][1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y + 1][1])
                        self.__boxes[y + 1][1].clickBox()

                    # Box to the right
                    if not self.__boxes[y][1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y][1])
                        self.__boxes[y][1].clickBox()

                # Right-most column (excluding corners)
                elif x == self.__width - 1 and 0 < y < self.__height - 1:
                    # Box directly above
                    if not self.__boxes[y - 1][-1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y - 1][-1])
                        self.__boxes[y - 1][-1].clickBox()

                    # Box directly below
                    if not self.__boxes[y + 1][-1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y + 1][-1])
                        self.__boxes[y + 1][-1].clickBox()

                    # Box to the top-left
                    if not self.__boxes[y - 1][-2].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y - 1][-2])
                        self.__boxes[y - 1][-2].clickBox()

                    # Box to the bottom-left
                    if not self.__boxes[y + 1][-2].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y + 1][-2])
                        self.__boxes[y + 1][-2].clickBox()
                    
                    # Box to the left
                    if not self.__boxes[y][-2].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[y][-2])
                        self.__boxes[y][-2].clickBox()

                # Top row (excluding corners)
                elif 0 < x < self.__width - 1 and y == 0:
                    # Box to the left
                    if not self.__boxes[0][x - 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[0][x - 1])
                        self.__boxes[0][x - 1].clickBox()

                    # Box to the right
                    if not self.__boxes[0][x + 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[0][x + 1])
                        self.__boxes[0][x + 1].clickBox()

                    # Box to the bottom-left
                    if not self.__boxes[1][x - 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[1][x - 1])
                        self.__boxes[1][x - 1].clickBox()

                    # Box to the bottom-right
                    if not self.__boxes[1][x + 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[1][x + 1])
                        self.__boxes[1][x + 1].clickBox()

                    # Box directly below
                    if not self.__boxes[1][x].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[1][x])
                        self.__boxes[1][x].clickBox()
                
                # Bottom row (excluding corners)
                elif 0 < x < self.__width - 1 and y == self.__height - 1:
                    # Box to the left
                    if not self.__boxes[-1][x - 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-1][x - 1])
                        self.__boxes[-1][x - 1].clickBox()

                    # Box to the right
                    if not self.__boxes[-1][x + 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-1][x + 1])
                        self.__boxes[-1][x + 1].clickBox()

                    # Box to the top-left
                    if not self.__boxes[-2][x - 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-2][x - 1])
                        self.__boxes[-2][x - 1].clickBox()

                    # Box to the top-right
                    if not self.__boxes[-2][x + 1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-2][x + 1])
                        self.__boxes[-2][x + 1].clickBox()

                    # Box directly above
                    if not self.__boxes[-2][x].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-2][x])
                        self.__boxes[-2][x].clickBox()
                
                # Top-left corner
                elif x == 0 and y == 0:
                    # Box to the left
                    if not self.__boxes[0][1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[0][1])
                        self.__boxes[0][1].clickBox()

                    # Box directly below
                    if not self.__boxes[1][0].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[1][0])
                        self.__boxes[1][0].clickBox()

                    # Box to the bottom-right
                    if not self.__boxes[1][1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[1][1])
                        self.__boxes[1][1].clickBox()

                # Top-right corner
                elif x == 0 and y == self.__height - 1:
                    # Box to the right
                    if not self.__boxes[-1][1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-1][1])
                        self.__boxes[-1][1].clickBox()

                    # Box directly above
                    if not self.__boxes[-2][0].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-2][0])
                        self.__boxes[-2][0].clickBox()

                    # Box to the top-right
                    if not self.__boxes[-2][1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-2][1])
                        self.__boxes[-2][1].clickBox()

                # Bottom-left corner
                elif x == self.__width - 1 and y == 0:
                    # Box to the left
                    if not self.__boxes[0][-2].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[0][-2])
                        self.__boxes[0][-2].clickBox()

                    # Box directly below
                    if not self.__boxes[1][-1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[1][-1])
                        self.__boxes[1][-1].clickBox()

                    # Box to the bottom-left
                    if not self.__boxes[1][-2].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[1][-2])
                        self.__boxes[1][-2].clickBox()

                # Bottom-right corner
                elif x == self.__width - 1 and y == self.__height - 1:
                    # Box to the left
                    if not self.__boxes[-1][-2].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-1][-2])
                        self.__boxes[-1][-2].clickBox()

                    # Box directly above
                    if not self.__boxes[-2][-1].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-2][-1])
                        self.__boxes[-2][-1].clickBox()

                    # Box to the top-left
                    if not self.__boxes[-2][-2].wasClicked():
                        boxesToBeFlipped.append(self.__boxes[-2][-2])
                        self.__boxes[-2][-2].clickBox()

            # The first box in the list is removed from the list.
            boxesToBeFlipped.pop(0)


    # Identifies the box that was clicked using the provided coordinates.
    def __identifyClickedBox(self, coordinates):
        # If the coordinates are out of bounds, then no box can be returned.
        if self.__x < coordinates[0] < self.__x + self.__width * self.__boxSize and self.__y < coordinates[1] < self.__y + self.__height * self.__boxSize:
            # Aligns the clicked coordinates with the index of the box on the grid.
            return self.__boxes[(coordinates[1] - self.__y) // self.__boxSize][(coordinates[0] - self.__x) // self.__boxSize]
        else:
            # Out of bounds. No box could be returned.
            return None


    # Flags the mines on the grid.
    # Used only when there are no safe boxes left.
    def __flagMines(self):
        for row in self.__boxes:
            for box in row:
                if box.getValue() == 'X' and not box.isFlagged():
                    box.flipFlag()
                    self.__numberOfFlagsLeft = str(int(self.__numberOfFlagsLeft) - 1)


    # Flips the mines on the grid.
    # Used only when a mine has been clicked.
    def __flipMines(self):
        for row in self.__boxes:
            for box in row:
                if box.getValue() == 'X':
                    box.clickBox()
                    if box.isFlagged():
                        box.flipFlag()
                        self.__numberOfFlagsLeft = str(int(self.__numberOfFlagsLeft) + 1)


    # Checks for any safe boxes. If so, returns true. Otherwise, returns false.
    def __hasRemainingSafeBoxes(self):
        return self.__numberOfSafeBoxes > 0


    # Resets the grid, including the boxes.
    def __reset(self):
        for row in self.__boxes:
            for box in row:
                box.reset()
        self.__numberOfFlagsLeft = str(self.__numberOfMines)
        self.__numberOfSafeBoxes = (self.__width * self.__height) - self.__numberOfMines
        self.__clickEnabled = True
        self.__firstClick = True
        self.__clickedAllSafeBoxes = False
        self.__clickedOnMine = False
        self.__gameOver = False
        self.__startTime = None
        self.__endTime = None


    # Public functions


    # User inputs are received and processed.
    def checkInputs(self):
        # The program continues unless the user presses the ESC key or closes the window.
        continueProgram = True

        # Handles user inputs
        for event in pygame.event.get():
            # Pressing the ESC key or closing the window terminates the game.
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                continueProgram = False
            
            # Right mouse click flags/unflags a box if it's not already clicked.
            # This is initially disabled until the user left-clicks a box.
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.__clickEnabled and not self.__firstClick:
                pos = pygame.mouse.get_pos()
                box = self.__identifyClickedBox(pos)

                # If the box hasn't been right-clicked already, 
                # then the box is flagged if it hasn't and vice versa.
                # The number of flags increments if a flag is removed or decrements if a flag is placed.
                if box != None and not box.wasClicked():
                    # Flags the box and decrements the number of flags left by 1.
                    if not box.isFlagged() and 0 < int(self.__numberOfFlagsLeft):
                        self.__numberOfFlagsLeft = str(int(self.__numberOfFlagsLeft) - 1)
                        box.flipFlag()
                    
                    # Unflags the box and increments the number of flags left by 1.
                    elif box.isFlagged() and int(self.__numberOfFlagsLeft) < self.__numberOfMines:
                        self.__numberOfFlagsLeft = str(int(self.__numberOfFlagsLeft) + 1)
                        box.flipFlag()

            # Left mouse click shows the box's value.
            # If it's the first click, the mines are deployed. (the 1st clicked box will not be a mine)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.__clickEnabled:
                pos = pygame.mouse.get_pos()
                box = self.__identifyClickedBox(pos)

                if box != None and not box.wasClicked():
                    # If it's the first click, then the mines are randomly deployed and the start time is recorded.
                    if self.__firstClick:
                        self.__deployMines(box)
                        self.__firstClick = False
                        self.__startTime = time()

                    # Flips the box to reveal its value.
                    # If the box has no value, then the adjacent boxes are opened.
                    self.__flipBox(box)

                    # If the clicked box is a mine, then the clickedOnMine variable flips to True.
                    # If not, then the grid is checked for any remaining safe boxes. 
                    # If none remain, the player wins.
                    if box.getValue() == 'X':
                        self.__clickedOnMine = True
                        self.__clickEnabled = False
                        self.__flipMines()
                    elif not self.__hasRemainingSafeBoxes():
                        self.__endTime = time()
                        self.__clickEnabled = False
                        self.__clickedAllSafeBoxes = True
                        self.__flagMines()

            # Spacebar resets the grid.
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__reset()

        return continueProgram

    
    # Draws the the boxes and lines that make up the grid.
    # NOTE: The screen must be updated for the grid to appear on the screen.
    def draw(self, window):
        # Makes the entire screen grey.
        window.fill(GREY)

        # Draws each box.
        for row in self.__boxes:
            for box in row:
                box.draw(window, self.__boxValueFont)

        # Variables needed to draw the gridlines.
        gridPixelWidth = self.__width * self.__boxSize
        gridPixelHeight = self.__height * self.__boxSize

        # Draws the horizontal gridlines.
        for x in range(self.__x, self.__x + gridPixelWidth + 1, self.__boxSize):
            pygame.draw.line(window, BLACK, (x, self.__y), (x, self.__y + gridPixelHeight))

        # Draws the vertical gridlines.
        for y in range(self.__y, self.__y + gridPixelHeight + 1, self.__boxSize):
            pygame.draw.line(window, BLACK, (self.__x, y), (self.__x + gridPixelWidth, y))


    # Returns the number of available flags.
    def getNumberOfFlagsLeft(self):
        return self.__numberOfFlagsLeft


    # Checks if all the safe boxes have been clicked.
    def clickedAllSafeBoxes(self):
        return self.__clickedAllSafeBoxes
    

    # Checks if a mine was clicked.
    def clickedOnMine(self):
        return self.__clickedOnMine


    # Checks if the game is over.
    def isGameOver(self):
        return self.__gameOver


    # Ends the game until it's reset.
    def gameOver(self):
        self.__gameOver = True


    # Returns the time elapsed since the game started.
    def getGameTime(self):
        return round(self.__endTime - self.__startTime, 2)
