'''
Justin Farnsworth
Minesweeper
February 12, 2020

pyinstaller -w -F minesweeper.py

'''

# Imported modules
import pygame
import tkinter
import sys
from levels import *
from tkinter import messagebox
from grid import Grid
from config import *


# If a level number is specified, then the game will modify the constants based on the number.
# For a custom level, all 8 values must be presented.
if len(sys.argv) == 2:
    ARGUMENTS = getLevel(int(sys.argv[1]))
    WINDOW_WIDTH, WINDOW_HEIGHT = ARGUMENTS[0], ARGUMENTS[1]
    GRID_X, GRID_Y = ARGUMENTS[2], ARGUMENTS[3]
    GRID_WIDTH, GRID_HEIGHT = ARGUMENTS[4], ARGUMENTS[5]
    NUMBER_OF_MINES = ARGUMENTS[6]
    BOX_SIZE = ARGUMENTS[7]
    del ARGUMENTS
elif len(sys.argv) == 9:
    WINDOW_WIDTH, WINDOW_HEIGHT = int(sys.argv[1]), int(sys.argv[2])
    GRID_X, GRID_Y = int(sys.argv[3]), int(sys.argv[4])
    GRID_WIDTH, GRID_HEIGHT = int(sys.argv[5]), int(sys.argv[6])
    NUMBER_OF_MINES = int(sys.argv[7])
    BOX_SIZE = int(sys.argv[8])


# Modifies windowWidth and windowHeight so that it aligns with the dimensions of the grid.
WINDOW_WIDTH = (WINDOW_WIDTH // BOX_SIZE) * BOX_SIZE
WINDOW_HEIGHT = (WINDOW_HEIGHT // BOX_SIZE) * BOX_SIZE


# Assertions set to ensure the game runs properly.
assert WINDOW_WIDTH >= 300 and WINDOW_WIDTH >= BOX_SIZE * 15
assert WINDOW_HEIGHT >= 200
assert GRID_X >= 0
assert GRID_Y >= BOX_SIZE * 2
assert GRID_WIDTH >= 6
assert GRID_HEIGHT >= 6
assert 1 <= NUMBER_OF_MINES <= 0.3 * (GRID_WIDTH * GRID_HEIGHT)
assert BOX_SIZE >= 20
assert GRID_X + (GRID_WIDTH * BOX_SIZE) <= WINDOW_WIDTH
assert GRID_Y + (GRID_HEIGHT * BOX_SIZE) + (BOX_SIZE * 2) <= WINDOW_HEIGHT


# Converts the integer value of NUMBER_OF_MINES into a string and saves it.
# Used for displaying the number of mines on the screen.
STRING_NUMBER_OF_MINES = f"{NUMBER_OF_MINES}"


# Draws the HUD.
def drawHeader(window, largeFont, smallFont, numberOfFlagsLeft):
    # Text to be printed on the screen.
    numberOfMinesInfo = largeFont.render("Mines: " + STRING_NUMBER_OF_MINES, True, BLACK)
    flagInfo = largeFont.render("Flags: " + numberOfFlagsLeft, True, BLACK)
    leftClickInfo = smallFont.render("Left Click: Open Box", True, BLACK)
    rightClickInfo = smallFont.render("Right Click: Flag Box", True, BLACK)
    spacebarInfo = smallFont.render("Spacebar: Reset Game", True, BLACK)
    escapeKeyInfo = smallFont.render("ESC Key: Exit Game", True, BLACK)

    # Prints the text directly above.
    window.blit(flagInfo, (5, 0))
    window.blit(numberOfMinesInfo, ((WINDOW_WIDTH - numberOfMinesInfo.get_width()) - 5, 0))
    window.blit(leftClickInfo, (5, WINDOW_HEIGHT - (BOX_SIZE * 2)))
    window.blit(rightClickInfo, (5, WINDOW_HEIGHT - BOX_SIZE))
    window.blit(spacebarInfo, (WINDOW_WIDTH - spacebarInfo.get_width() - 5, WINDOW_HEIGHT - (BOX_SIZE * 2)))
    window.blit(escapeKeyInfo, (WINDOW_WIDTH - escapeKeyInfo.get_width() - 5, WINDOW_HEIGHT - BOX_SIZE))
    

# Sets up the message box for winning/losing condition.
def messageBox(subject, content):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


# Prints losing message.
def losingMessage():
    messageBox("You lost!", "You lost...\nTry again!")


# Prints winning message.
def winningMessage(time):
    messageBox("You won!", f"Congratulations!\nTime: {time} seconds")


# Main function initializes the game.
def main():
    # Initializes pygame and sets the name of window.
    pygame.init()
    pygame.display.set_caption('Minesweeper')

    # Sets the window dimensions and clock.
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Initializes the font for the HUD.
    largeFont = pygame.font.SysFont('arial', int(BOX_SIZE * 1.6))
    smallFont = pygame.font.SysFont('arial', int(BOX_SIZE * 0.8))

    # Initalizes the grid.
    boxes = Grid(GRID_WIDTH, GRID_HEIGHT, BOX_SIZE, NUMBER_OF_MINES, GRID_X, GRID_Y)

    # Determines if the game continues or terminates.
    continueProgram = True
    
    # Main loop
    # Checks and processes user inputs.
    while continueProgram:
        # FPS set to 30.
        clock.tick(30)
        
        # Checks for inputs and determines if the game continues.
        continueProgram = boxes.checkInputs()

        # Makes the entire screen grey.
        window.fill(WHITE)
        
        # Draws the grid.
        boxes.draw(window)

        # Draws the title and other text.
        drawHeader(window, largeFont, smallFont, boxes.getNumberOfFlagsLeft())

        # Updates the screen to show the frame.
        pygame.display.update()

        # Player wins if no safe boxes remain.
        # Player loses if a mine is clicked.
        if not boxes.isGameOver():
            if boxes.clickedAllSafeBoxes():
                winningMessage(boxes.getGameTime())
                boxes.gameOver()
            elif boxes.clickedOnMine():
                losingMessage()
                boxes.gameOver()


# Executes program.
if __name__ == '__main__':
    main()
