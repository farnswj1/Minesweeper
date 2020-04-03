#Imported modules
import pygame
import sys
from random import randint
from time import time
from box import Box


#Colors
GREY = (192, 192, 192)
BLACK = (0, 0, 0)


#Grid class
class Grid(object):
    #Constructor
    def __init__(self, width, height, boxSize, numberOfMines, x = 0, y = 0):
        self.boxes = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.boxSize = boxSize
        self.numberOfMines = numberOfMines
        self.boxValueFont = pygame.font.SysFont('arial', boxSize)
        self.numberOfFlagsLeft = str(numberOfMines)
        self.numberOfSafeBoxes = (width * height) - numberOfMines
        self.clickEnabled = True
        self.firstClick = True
        self.clickedAllSafeBoxes = False
        self.clickedOnMine = False
        self.gameOver = False
        self.startTime = None
        self.endTime = None

        #Intializes the boxes for the grid
        for y in range(self.y, self.y + self.height * self.boxSize, self.boxSize):
            row = []
            for x in range(self.x, self.x + self.width * self.boxSize, self.boxSize):
                row.append(Box(x, y, self.boxSize))
            self.boxes.append(row)


    #Randomly places a specified number of mines on the grid
    #The clicked box are its adjacent boxes are excluded from being a potential mine
    def deployMines(self, box):
        #Calculates the index of the box
        boxIndexOnGridX = (box.x - self.x) // self.boxSize
        boxIndexOnGridY = (box.y - self.y) // self.boxSize

        #Deploys the mines
        for i in range(self.numberOfMines):
            mineDeployed = False
            
            #Loop repeats until a mine has its own coordinates
            while not mineDeployed:
                x = randint(0, self.width - 1)
                y = randint(0, self.height - 1)

                #Checks if box[y][x] is adjacent to the clicked box. If so, then x and y are randomly generated again.
                if not boxIndexOnGridX - 1 <= x <= boxIndexOnGridX + 1 or not boxIndexOnGridY - 1 <= y <= boxIndexOnGridY + 1:
                    #Saves the value of the box as a mine if current box isn't already one
                    #The while loop is also terminated
                    if self.boxes[y][x].value != 'X':
                        self.boxes[y][x].value = 'X'
                        mineDeployed = True
        
        #All boxes count the number of adjacent mines and their respective values are saved
        for y in range(self.height):
            for x in range(self.width):
                #If the current box is a mine, then the counting is skipped for this box
                if self.boxes[y][x].value != 'X':
                    adjacentMines = 0

                    #Interior boxes
                    if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                        if self.boxes[y - 1][x].value == 'X': adjacentMines += 1     #Box directly above
                        if self.boxes[y + 1][x].value == 'X': adjacentMines += 1     #Box directly below
                        if self.boxes[y][x - 1].value == 'X': adjacentMines += 1     #Box to the left
                        if self.boxes[y][x + 1].value == 'X': adjacentMines += 1     #Box to the right
                        if self.boxes[y - 1][x - 1].value == 'X': adjacentMines += 1 #Box to the top-left
                        if self.boxes[y - 1][x + 1].value == 'X': adjacentMines += 1 #Box to the top-right
                        if self.boxes[y + 1][x - 1].value == 'X': adjacentMines += 1 #Box to the bottom-left
                        if self.boxes[y + 1][x + 1].value == 'X': adjacentMines += 1 #Box to the bottom-right
                    
                    #Left-most column (excluding corners)
                    elif x == 0 and 0 < y < self.height - 1:
                        if self.boxes[y - 1][0].value == 'X': adjacentMines += 1 #Box directly above
                        if self.boxes[y + 1][0].value == 'X': adjacentMines += 1 #Box directly below
                        if self.boxes[y - 1][1].value == 'X': adjacentMines += 1 #Box to the top-right
                        if self.boxes[y + 1][1].value == 'X': adjacentMines += 1 #Box to the bottom-right
                        if self.boxes[y][1].value == 'X': adjacentMines += 1     #Box to the right

                    #Right-most column (excluding corners)
                    elif x == self.width - 1 and 0 < y < self.height - 1:
                        if self.boxes[y - 1][-1].value == 'X': adjacentMines += 1 #Box directly above
                        if self.boxes[y + 1][-1].value == 'X': adjacentMines += 1 #Box directly below
                        if self.boxes[y - 1][-2].value == 'X': adjacentMines += 1 #Box to the top-left
                        if self.boxes[y + 1][-2].value == 'X': adjacentMines += 1 #Box to the bottom-left
                        if self.boxes[y][-2].value == 'X': adjacentMines += 1     #Box to the left

                    #Top row (excluding corners)
                    elif 0 < x < self.width - 1 and y == 0:
                        if self.boxes[0][x - 1].value == 'X': adjacentMines += 1 #Box to the left
                        if self.boxes[0][x + 1].value == 'X': adjacentMines += 1 #Box to the right
                        if self.boxes[1][x - 1].value == 'X': adjacentMines += 1 #Box to the bottom-left
                        if self.boxes[1][x + 1].value == 'X': adjacentMines += 1 #Box to the bottom-right
                        if self.boxes[1][x].value == 'X': adjacentMines += 1     #Box directly below

                    #Bottom row (excluding corners)
                    elif 0 < x < self.width - 1 and y == self.height - 1:
                        if self.boxes[-1][x - 1].value == 'X': adjacentMines += 1 #Box to the left
                        if self.boxes[-1][x + 1].value == 'X': adjacentMines += 1 #Box to the right
                        if self.boxes[-2][x - 1].value == 'X': adjacentMines += 1 #Box to the top-left
                        if self.boxes[-2][x + 1].value == 'X': adjacentMines += 1 #Box to the top-right
                        if self.boxes[-2][x].value == 'X': adjacentMines += 1     #Box directly above

                    #Top-left corner
                    elif x == 0 and y == 0:
                        if self.boxes[0][1].value == 'X': adjacentMines += 1 #Box to the right
                        if self.boxes[1][0].value == 'X': adjacentMines += 1 #Box directly below
                        if self.boxes[1][1].value == 'X': adjacentMines += 1 #Box to the bottom-right

                    #Top-right corner
                    elif x == 0 and y == self.height - 1:
                        if self.boxes[-1][1].value == 'X': adjacentMines += 1 #Box to the right
                        if self.boxes[-2][0].value == 'X': adjacentMines += 1 #Box directly above
                        if self.boxes[-2][1].value == 'X': adjacentMines += 1 #Box to the top-right

                    #Bottom-left corner
                    elif x == self.width - 1 and y == 0:
                        if self.boxes[0][-2].value == 'X': adjacentMines += 1 #Box to the left
                        if self.boxes[1][-1].value == 'X': adjacentMines += 1 #Box directly below
                        if self.boxes[1][-2].value == 'X': adjacentMines += 1 #Box to the bottom-left

                    #Bottom-right corner
                    elif x == self.width - 1 and y == self.height - 1:
                        if self.boxes[-1][-2].value == 'X': adjacentMines += 1 #Box to the left
                        if self.boxes[-2][-1].value == 'X': adjacentMines += 1 #Box directly above
                        if self.boxes[-2][-2].value == 'X': adjacentMines += 1 #Box to the top-left
                    
                    #Updates the value of the box by saving the number of adjacent mines
                    self.boxes[y][x].updateValue(adjacentMines)


    #Iteratively shows the value of boxes
    #If the box has no value, then the adjacent boxes are also flipped
    #Base case is when the value of the box's value is not a number or 'X'
    def flipBox(self, clickedBox):
        #Creates a list of boxes that will be flipped. The clicked box inserted
        boxesToBeFlipped = [clickedBox]
        clickedBox.clicked = True

        #The loop repeats until the list is empty
        while len(boxesToBeFlipped) > 0:
            box = boxesToBeFlipped[0]
            
            #If the box isn't a mine, then the number of safe boxes remaining decreases by 1
            if box.value != 'X':
                self.numberOfSafeBoxes -= 1

            #If the clicked box was flagged, then the number of flags left increases by 1
            if box.flagged:
                box.flagged = False
                self.numberOfFlagsLeft = str(int(self.numberOfFlagsLeft) + 1)

            #If the box has no value, then the adjacent boxes are added if not clicked already
            if box.value == '0':
                x, y = (box.x - self.x) // self.boxSize, (box.y - self.y) // self.boxSize

                #Interior boxes
                if 0 < x < self.width - 1 and 0 < y < self.height - 1:
                    #Box directly above
                    if not self.boxes[y - 1][x].clicked:
                        boxesToBeFlipped.append(self.boxes[y - 1][x])
                        self.boxes[y - 1][x].clicked = True

                    #Box directly below
                    if not self.boxes[y + 1][x].clicked:
                        boxesToBeFlipped.append(self.boxes[y + 1][x])
                        self.boxes[y + 1][x].clicked = True

                    #Box to the left
                    if not self.boxes[y][x - 1].clicked:
                        boxesToBeFlipped.append(self.boxes[y][x - 1])
                        self.boxes[y][x - 1].clicked = True

                    #Box to the right
                    if not self.boxes[y][x + 1].clicked:
                        boxesToBeFlipped.append(self.boxes[y][x + 1])
                        self.boxes[y][x + 1].clicked = True

                    #Box to the top-left
                    if not self.boxes[y - 1][x - 1].clicked:
                        boxesToBeFlipped.append(self.boxes[y - 1][x - 1])
                        self.boxes[y - 1][x - 1].clicked = True

                    #Box to the top-right
                    if not self.boxes[y - 1][x + 1].clicked:
                        boxesToBeFlipped.append(self.boxes[y - 1][x + 1])
                        self.boxes[y - 1][x + 1].clicked = True

                    #Box to the bottom-left
                    if not self.boxes[y + 1][x - 1].clicked:
                        boxesToBeFlipped.append(self.boxes[y + 1][x - 1])
                        self.boxes[y + 1][x - 1].clicked = True

                    #Box to the bottom-right
                    if not self.boxes[y + 1][x + 1].clicked:
                        boxesToBeFlipped.append(self.boxes[y + 1][x + 1])
                        self.boxes[y + 1][x + 1].clicked = True

                #Left-most column (excluding corners)
                elif x == 0 and 0 < y < self.height - 1:
                    #Box directly above
                    if not self.boxes[y - 1][0].clicked:
                        boxesToBeFlipped.append(self.boxes[y - 1][0])
                        self.boxes[y - 1][0].clicked = True

                    #Box directly below
                    if not self.boxes[y + 1][0].clicked:
                        boxesToBeFlipped.append(self.boxes[y + 1][0])
                        self.boxes[y + 1][0].clicked = True

                    #Box to the top-right
                    if not self.boxes[y - 1][1].clicked:
                        boxesToBeFlipped.append(self.boxes[y - 1][1])
                        self.boxes[y - 1][1].clicked = True

                    #Box to the bottom-right
                    if not self.boxes[y + 1][1].clicked:
                        boxesToBeFlipped.append(self.boxes[y + 1][1])
                        self.boxes[y + 1][1].clicked = True

                    #Box to the right
                    if not self.boxes[y][1].clicked:
                        boxesToBeFlipped.append(self.boxes[y][1])
                        self.boxes[y][1].clicked = True

                #Right-most column (excluding corners)
                elif x == self.width - 1 and 0 < y < self.height - 1:
                    #Box directly above
                    if not self.boxes[y - 1][-1].clicked:
                        boxesToBeFlipped.append(self.boxes[y - 1][-1])
                        self.boxes[y - 1][-1].clicked = True

                    #Box directly below
                    if not self.boxes[y + 1][-1].clicked:
                        boxesToBeFlipped.append(self.boxes[y + 1][-1])
                        self.boxes[y + 1][-1].clicked = True

                    #Box to the top-left
                    if not self.boxes[y - 1][-2].clicked:
                        boxesToBeFlipped.append(self.boxes[y - 1][-2])
                        self.boxes[y - 1][-2].clicked = True

                    #Box to the bottom-left
                    if not self.boxes[y + 1][-2].clicked:
                        boxesToBeFlipped.append(self.boxes[y + 1][-2])
                        self.boxes[y + 1][-2].clicked = True
                    
                    #Box to the left
                    if not self.boxes[y][-2].clicked:
                        boxesToBeFlipped.append(self.boxes[y][-2])
                        self.boxes[y][-2].clicked = True

                #Top row (excluding corners)
                elif 0 < x < self.width - 1 and y == 0:
                    #Box to the left
                    if not self.boxes[0][x - 1].clicked:
                        boxesToBeFlipped.append(self.boxes[0][x - 1])
                        self.boxes[0][x - 1].clicked = True

                    #Box to the right
                    if not self.boxes[0][x + 1].clicked:
                        boxesToBeFlipped.append(self.boxes[0][x + 1])
                        self.boxes[0][x + 1].clicked = True

                    #Box to the bottom-left
                    if not self.boxes[1][x - 1].clicked:
                        boxesToBeFlipped.append(self.boxes[1][x - 1])
                        self.boxes[1][x - 1].clicked = True

                    #Box to the bottom-right
                    if not self.boxes[1][x + 1].clicked:
                        boxesToBeFlipped.append(self.boxes[1][x + 1])
                        self.boxes[1][x + 1].clicked = True

                    #Box directly below
                    if not self.boxes[1][x].clicked:
                        boxesToBeFlipped.append(self.boxes[1][x])
                        self.boxes[1][x].clicked = True
                
                #Bottom row (excluding corners)
                elif 0 < x < self.width - 1 and y == self.height - 1:
                    #Box to the left
                    if not self.boxes[-1][x - 1].clicked:
                        boxesToBeFlipped.append(self.boxes[-1][x - 1])
                        self.boxes[-1][x - 1].clicked = True

                    #Box to the right
                    if not self.boxes[-1][x + 1].clicked:
                        boxesToBeFlipped.append(self.boxes[-1][x + 1])
                        self.boxes[-1][x + 1].clicked = True

                    #Box to the top-left
                    if not self.boxes[-2][x - 1].clicked:
                        boxesToBeFlipped.append(self.boxes[-2][x - 1])
                        self.boxes[-2][x - 1].clicked = True

                    #Box to the top-right
                    if not self.boxes[-2][x + 1].clicked:
                        boxesToBeFlipped.append(self.boxes[-2][x + 1])
                        self.boxes[-2][x + 1].clicked = True

                    #Box directly above
                    if not self.boxes[-2][x].clicked:
                        boxesToBeFlipped.append(self.boxes[-2][x])
                        self.boxes[-2][x].clicked = True
                
                #Top-left corner
                elif x == 0 and y == 0:
                    #Box to the left
                    if not self.boxes[0][1].clicked:
                        boxesToBeFlipped.append(self.boxes[0][1])
                        self.boxes[0][1].clicked = True

                    #Box directly below
                    if not self.boxes[1][0].clicked:
                        boxesToBeFlipped.append(self.boxes[1][0])
                        self.boxes[1][0].clicked = True

                    #Box to the bottom-right
                    if not self.boxes[1][1].clicked:
                        boxesToBeFlipped.append(self.boxes[1][1])
                        self.boxes[1][1].clicked = True

                #Top-right corner
                elif x == 0 and y == self.height - 1:
                    #Box to the right
                    if not self.boxes[-1][1].clicked:
                        boxesToBeFlipped.append(self.boxes[-1][1])
                        self.boxes[-1][1].clicked = True

                    #Box directly above
                    if not self.boxes[-2][0].clicked:
                        boxesToBeFlipped.append(self.boxes[-2][0])
                        self.boxes[-2][0].clicked = True

                    #Box to the top-right
                    if not self.boxes[-2][1].clicked:
                        boxesToBeFlipped.append(self.boxes[-2][1])
                        self.boxes[-2][1].clicked = True

                #Bottom-left corner
                elif x == self.width - 1 and y == 0:
                    #Box to the left
                    if not self.boxes[0][-2].clicked:
                        boxesToBeFlipped.append(self.boxes[0][-2])
                        self.boxes[0][-2].clicked = True

                    #Box directly below
                    if not self.boxes[1][-1].clicked:
                        boxesToBeFlipped.append(self.boxes[1][-1])
                        self.boxes[1][-1].clicked = True

                    #Box to the bottom-left
                    if not self.boxes[1][-2].clicked:
                        boxesToBeFlipped.append(self.boxes[1][-2])
                        self.boxes[1][-2].clicked = True

                #Bottom-right corner
                elif x == self.width - 1 and y == self.height - 1:
                    #Box to the left
                    if not self.boxes[-1][-2].clicked:
                        boxesToBeFlipped.append(self.boxes[-1][-2])
                        self.boxes[-1][-2].clicked = True

                    #Box directly above
                    if not self.boxes[-2][-1].clicked:
                        boxesToBeFlipped.append(self.boxes[-2][-1])
                        self.boxes[-2][-1].clicked = True

                    #Box to the top-left
                    if not self.boxes[-2][-2].clicked:
                        boxesToBeFlipped.append(self.boxes[-2][-2])
                        self.boxes[-2][-2].clicked = True

            #The first box in the list is removed from the list
            boxesToBeFlipped.pop(0)


    #Identifies the box that was clicked using the provided coordinates
    def identifyClickedBox(self, coordinates):
        #If the coordinates are out of bounds, then no box can be returned
        if self.x < coordinates[0] < self.x + self.width * self.boxSize and self.y < coordinates[1] < self.y + self.height * self.boxSize:
            #Aligns the clicked coordinates with the index of the box on the grid
            return self.boxes[(coordinates[1] - self.y) // self.boxSize][(coordinates[0] - self.x) // self.boxSize]
        else:
            #Out of bounds. No box could be returned
            return None


    #User inputs are received and processed.
    def checkInputs(self):
        for event in pygame.event.get():
            #Pressing the ESC key or closing the window terminates the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            #Right mouse click flags/unflags a box if it's not already clicked
            #This is initially disabled until the user left-clicks a box
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.clickEnabled and not self.firstClick:
                pos = pygame.mouse.get_pos()
                box = self.identifyClickedBox(pos)

                #If the box hasn't been right-clicked already, then the box is flagged if it hasn't and vice versa
                #The number of flags increments if a flag is removed or decrements if a flag is placed
                if box != None and not box.clicked:
                    #Flags the box and decrements the number of flags left by 1
                    if not box.flagged and 0 < int(self.numberOfFlagsLeft):
                        self.numberOfFlagsLeft = str(int(self.numberOfFlagsLeft) - 1)
                        box.flipFlag()
                    
                    #Unflags the box and increments the number of flags left by 1
                    elif box.flagged and int(self.numberOfFlagsLeft) < self.numberOfMines:
                        self.numberOfFlagsLeft = str(int(self.numberOfFlagsLeft) + 1)
                        box.flipFlag()

            #Left mouse click shows the box's value
            #If it's the first click, the mines are deployed (the 1st clicked box will not be a mine)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.clickEnabled:
                pos = pygame.mouse.get_pos()
                box = self.identifyClickedBox(pos)

                if box != None:
                    #If it's the first click, then the mines are randomly deployed and the start time is recorded
                    if self.firstClick:
                        self.deployMines(box)
                        self.firstClick = False
                        self.startTime = time()

                    #Flips the box to reveal its value
                    #If the box has no value, then the adjacent boxes are opened
                    self.flipBox(box)

                    #If the clicked box is a mine, then the clickedOnMine variable flips to True
                    #If not, then the grid is checked for any remaining safe boxes. If none remain, the player wins
                    if box.value == 'X':
                        self.clickedOnMine = True
                        self.clickEnabled = False
                        self.flipMines()
                    elif not self.hasRemainingSafeBoxes():
                        self.endTime = time()
                        self.clickEnabled = False
                        self.clickedAllSafeBoxes = True
                        self.flagMines()

            #Space button resets the grid
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

    
    #Draws the the boxes and lines that make up the grid
    #NOTE: The screen must be updated for the grid to appear on the screen
    def draw(self, window):
        #Makes the entire screen grey
        window.fill(GREY)

        #Draws each box
        for row in self.boxes:
            for box in row:
                box.draw(window, self.boxValueFont)

        #Variables needed to draw the gridlines
        gridPixelWidth = self.width * self.boxSize
        gridPixelHeight = self.height * self.boxSize

        #Draws the horizontal gridlines
        for x in range(self.x, self.x + gridPixelWidth + 1, self.boxSize):
            pygame.draw.line(window, BLACK, (x, self.y), (x, self.y + gridPixelHeight))

        #Draws the vertical gridlines
        for y in range(self.y, self.y + gridPixelHeight + 1, self.boxSize):
            pygame.draw.line(window, BLACK, (self.x, y), (self.x + gridPixelWidth, y))

        #Displays the grid on the screen
        #pygame.display.update()


    #Flags the mines on the grid
    #Used only when there are no safe boxes left
    def flagMines(self):
        for row in self.boxes:
            for box in row:
                if box.value == 'X' and not box.flagged:
                    box.flipFlag()
                    self.numberOfFlagsLeft = str(int(self.numberOfFlagsLeft) - 1)


    #Flips the mines on the grid
    #Used only when a mine has been clicked
    def flipMines(self):
        for row in self.boxes:
            for box in row:
                if box.value == 'X':
                    box.clicked = True
                    if box.flagged:
                        box.flagged = False
                        self.numberOfFlagsLeft = str(int(self.numberOfFlagsLeft) + 1)


    #Checks for any safe boxes. If so, returns true. Otherwise, returns false
    def hasRemainingSafeBoxes(self):
        return self.numberOfSafeBoxes > 0


    #Returns the time elapsed since the game started
    def getGameTime(self):
        return round(self.endTime - self.startTime, 2)


    #Resets the grid, including the boxes
    def reset(self):
        for row in self.boxes:
            for box in row:
                box.reset()
        self.numberOfFlagsLeft = str(self.numberOfMines)
        self.numberOfSafeBoxes = (self.width * self.height) - self.numberOfMines
        self.clickEnabled = True
        self.firstClick = True
        self.clickedAllSafeBoxes = False
        self.clickedOnMine = False
        self.gameOver = False
        self.startTime = None
        self.endTime = None
