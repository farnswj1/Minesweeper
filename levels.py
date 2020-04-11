'''
Justin Farnsworth
Minesweeper Levels
February 12, 2020

'''

# Returns a list of values representing the following:
# [window width, 
#  window height, 
#  grid x-value, 
#  grid y-value, 
#  grid width, 
#  grid height, 
#  # of mines, 
#  box size]
def getLevel(levelNumber):
    args = []

    if   levelNumber == 1: args = [ 600, 540, 120, 80,  9,  9,   10, 40] # Easy
    elif levelNumber == 2: args = [ 600, 600,  60, 60, 16, 16,   40, 30] # Medium
    elif levelNumber == 3: args = [ 900, 600,   0, 60, 30, 16,  100, 30] # Hard
    elif levelNumber == 4: args = [ 720, 672,   0, 48, 30, 24,  200, 24] # Expert
    elif levelNumber == 5: args = [1200, 680,   0, 40, 60, 30,  500, 20] # Insane
    elif levelNumber == 6: args = [1800, 880,   0, 40, 90, 40, 1000, 20] # Impossible
    else:                  args = [ 600, 600,   0, 60, 20, 16,   30, 30] # Default

    return args
