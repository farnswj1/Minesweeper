'''
Justin Farnsworth
Minesweeper Box
February 12, 2020

'''

# Imported modules
import pygame
from config import *


# Box class
class Box(object):
    # Constructor
    def __init__(self, positionX, positionY, size):
        self.__x = positionX
        self.__y = positionY
        self.__size = size
        self.__value = None
        self.__clicked = False
        self.__flagged = False


    # Draws the box and/or its value.
    def draw(self, window, valueFont):
        # If the box is not clicked, then the box will be either dim grey or orange.
        if not self.__clicked:
            # If the box is not flagged, then the box is dim grey. Otherwise, it's orange.
            if self.__flagged:
                pygame.draw.rect(window, ORANGE, (self.__x, self.__y, self.__size - 1, self.__size - 1))
            else:
                pygame.draw.rect(window, DIM_GREY, (self.__x, self.__y, self.__size - 1, self.__size - 1))

        # If the box has a value, then the value is displayed except for 0.
        elif self.__value != '0':
            if self.__value == 'X': # This is the value for a mine.
                pygame.draw.rect(window, RED, (self.__x, self.__y, self.__size - 1, self.__size - 1))
                boxValue = valueFont.render(self.__value, True, BLACK)
            elif self.__value == '1':
                boxValue = valueFont.render(self.__value, True, BLUE)
            elif self.__value == '2':
                boxValue = valueFont.render(self.__value, True, GREEN)
            elif self.__value == '3':
                boxValue = valueFont.render(self.__value, True, MAROON)
            elif self.__value == '4':
                boxValue = valueFont.render(self.__value, True, PURPLE)
            elif self.__value == '5':
                boxValue = valueFont.render(self.__value, True, BRICK_RED)
            elif self.__value == '6':
                boxValue = valueFont.render(self.__value, True, DARK_CYAN)
            elif self.__value == '7':
                boxValue = valueFont.render(self.__value, True, BLACK)
            elif self.__value == '8':
                boxValue = valueFont.render(self.__value, True, DIM_GREY)

            # The value of the box is drawn onto the screen.
            window.blit(boxValue, (self.__x + ((self.__size - boxValue.get_width()) // 2), self.__y + ((self.__size - boxValue.get_height()) // 2)))


    # Retrieves the current position of the box on the x-axis.
    def getX(self):
        return self.__x

    
    # Retrieves the current position of the box on the y-axis.
    def getY(self):
        return self.__y


    # Retrieves the current value of the box.
    def getValue(self):
        return self.__value
    

    # Updates the current value of the box.
    def updateValue(self, value):
        self.__value = str(value)


    # Sets clicked to True.
    def clickBox(self):
        self.__clicked = True


    # Checks is the box has already been clicked.
    def wasClicked(self):
        return self.__clicked


    # Flips the flagged variable.
    def flipFlag(self):
        self.__flagged = not self.__flagged
    

    # Checks is the box is flagged.
    def isFlagged(self):
        return self.__flagged


    # Resets the box to its defaults.
    def reset(self):
        self.__value = None
        self.__flagged = False
        self.__clicked = False
