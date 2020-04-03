#Imported modules
import pygame


#Colors
BLACK =     (  0,   0,   0)
DIM_GREY =  (112, 112, 112)
RED =       (255,   0 ,  0)
ORANGE =    (255, 160,   0)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 128,   0)
MAROON =    (204,  51,   0)
PURPLE =    (133,  16, 216)
BRICK_RED = (110,  16,   5)
DARK_CYAN = (  0, 160, 160)


#Box class
class Box(object):
    #Constructor
    def __init__(self, positionX, positionY, size):
        self.x = positionX
        self.y = positionY
        self.size = size
        self.value = None
        self.clicked = False
        self.flagged = False


    #Draws the box and/or its value
    def draw(self, window, valueFont):
        #If the box is not clicked, then the box will be either dim grey or orange
        if not self.clicked:
            #If the box is not flagged, then the box is dim grey. Otherwise, it's orange
            if self.flagged:
                pygame.draw.rect(window, ORANGE, (self.x, self.y, self.size - 1, self.size - 1))
            else:
                pygame.draw.rect(window, DIM_GREY, (self.x, self.y, self.size - 1, self.size - 1))

        #If the box has a value, then the value is displayed
        #Clicked boxes with no values are not drawn
        elif self.value != '0':
            if self.value == 'X': #This is the value for a mine
                pygame.draw.rect(window, RED, (self.x, self.y, self.size - 1, self.size - 1))
                boxValue = valueFont.render(self.value, True, BLACK)
            elif self.value == '1':
                boxValue = valueFont.render(self.value, True, BLUE)
            elif self.value == '2':
                boxValue = valueFont.render(self.value, True, GREEN)
            elif self.value == '3':
                boxValue = valueFont.render(self.value, True, MAROON)
            elif self.value == '4':
                boxValue = valueFont.render(self.value, True, PURPLE)
            elif self.value == '5':
                boxValue = valueFont.render(self.value, True, BRICK_RED)
            elif self.value == '6':
                boxValue = valueFont.render(self.value, True, DARK_CYAN)
            elif self.value == '7':
                boxValue = valueFont.render(self.value, True, BLACK)
            elif self.value == '8':
                boxValue = valueFont.render(self.value, True, DIM_GREY)

            #The value of the box is drawn onto the screen
            window.blit(boxValue, (self.x + ((self.size - boxValue.get_width()) // 2), self.y + ((self.size - boxValue.get_height()) // 2)))


    #Updates the current value of the box, unless the value is 0
    def updateValue(self, value):
        self.value = str(value)


    #Flips the flagged variable
    def flipFlag(self):
        self.flagged = not self.flagged


    #Resets the box to its defaults
    def reset(self):
        self.value = None
        self.flagged = False
        self.clicked = False
