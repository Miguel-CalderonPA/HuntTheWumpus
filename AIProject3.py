'''
Miguel Calderon
Date: 3/10/2021
CSC 535 Artificial Intelligence Project #3 Wumpus
Last Modification: 3/28/2021
Professor Ian MacDonald
'''
import board as b
import player as p
# CONSTANTS
FILE = "wumpus.txt"
VALID_MOVES = "RrLlFfSs"
VALID_PIECES = ["X", "W", "G", "P"]
STARTING_AMMO = 1
STARTING_X = 4
STARTING_Y = 1


# --------------------------------------------------------------------------------
# PRE: needs file, currently set to only use wumpus.txt
# POST: returns word list without punctuation
# PURPOSE: to read the file, remove the punctuation and store each word in a list
def readFile():
    error = True
    mode = "r"
    while error:
        #filename = input("Please enter the board for Wumpus: ")
        filename = FILE
        try:    # While open make all symbols uniform
            with open(filename, mode) as file:
                error = False
                board = file.read()
                board = board.upper()
                board = board.replace("\n", " ")
                board = board.split()
                for char in board:  # and verify correct symbols
                    if char not in VALID_PIECES:
                        error = True
        except FileNotFoundError: # if not found
            print("ERROR! You entered a wrong file name. Enter it again.")
            filename = input("Please enter the filename: ")
    return board
# --------------------------------------------------------------------------------
# PRE: N/A
# POST: Prints you won
# PURPOSE: to show the player they won
def PrintWon():
    print("____    ____  ______    __    __     ____    __    ____  ______   .__   __.  __   __   __")
    print("\   \  /   / /  __  \  |  |  |  |    \   \  /  \  /   / /  __  \  |  \ |  | |  | |  | |  | ")
    print(" \   \/   / |  |  |  | |  |  |  |     \   \/    \/   / |  |  |  | |   \|  | |  | |  | |  | ")
    print("  \_    _/  |  |  |  | |  |  |  |      \            /  |  |  |  | |  . `  | |  | |  | |  | ")
    print("    |  |    |  `--'  | |  `--'  |       \    /\    /   |  `--'  | |  |\   | |__| |__| |__| ")
    print("    |__|     \______/   \______/         \__/  \__/     \______/  |__| \__| (__) (__) (__) ")
# --------------------------------------------------------------------------------
# PRE: N/A
# POST: Prints you died
# PURPOSE: to show the player they died
def PrintDied():
    print("          _______             ______  _________ _______  ______          ")
    print("|\     /|(  ___  )|\     /|  (  __  \ \__   __/(  ____ \(  __  \         ")
    print("( \   / )| (   ) || )   ( |  | (  \  )   ) (   | (    \/| (  \  )        ")
    print(" \ (_) / | |   | || |   | |  | |   ) |   | |   | (__    | |   ) |        ")
    print("  \   /  | |   | || |   | |  | |   | |   | |   |  __)   | |   | |        ")
    print("   ) (   | |   | || |   | |  | |   ) |   | |   | (      | |   ) |        ")
    print("   | |   | (___) || (___) |  | (__/  )___) (___| (____/\| (__/  )_  _  _ ")
    print("   \_/   (_______)(_______)  (______/ \_______/(_______/(______/(_)(_)(_)")
# --------------------------------------------------------------------------------
# PRE: needs name
# POST: prints rules
# PURPOSE: prints the rules so the user knows what to do
def PrintRules(name):
    defaultName = "Person"
    defaultName = str(name)
    print("\nHello " + defaultName + "!")
    print("Welcome to HUNT THE WUMPUS! ")
    print("The goal of the game is to find the gold, but be careful of the wumpus,")
    print("You have one arrow, but you only get one shot!")
    print("Move around the caves until you die or get rich! ")
    print("To be clear the board coordinates are printed as [COL][ROW]")
# --------------------------------------------------------------------------------
# PRE: N/A
# POST: validates input from the user
# PURPOSE: determines the next move based on user input
def ValidateMove():
    Invalid = True
    while Invalid:
        move = input("What would you like to do? Please enter command [R,L,F,S]: ")
        if move in VALID_MOVES:  # makes input uniform and verifies input
            move = move.upper()
            move = move.strip()
            return move
        else:
            print("Invalid Move, please re-enter")
            move = input("What would you like to do? Please enter command [R,L,F,S]: ")
# --------------------------------------------------------------------------------

def main():
    values = readFile()  # read the values from the file
    theMap = b.Board()  # Instantiates the playing board
    name = input("Please enter you name: ")
    PrintRules(name)
    player = p.Player(name, STARTING_X, STARTING_Y, STARTING_AMMO)  # Instantiates the player
    theMap.__int__(values)
    theMap.BoardUpdate(player)  # updates player's condition in relation to the obstacles

    # while player isn't dead or hasn't won
    while player.getDead() == False and theMap.HasPlayerWon(player) == False:
        player.PrintKnowledge()                         # Print hints and add to Knowledge base
        move = ValidateMove()
        if move == "R":                                 # if player choose to face right of current position
            if player.getDirection() == "EAST":
                player.setDirection("SOUTH")
            elif player.getDirection() == "SOUTH":
                player.setDirection("WEST")
            elif player.getDirection() == "WEST":
                player.setDirection("NORTH")
            elif player.getDirection() == "NORTH":
                player.setDirection("EAST")
            else:
                print("ERROR")
        elif move == "L":                              # if player choose to face left of current position
            if player.getDirection() == "EAST":
                player.setDirection("NORTH")
            elif player.getDirection() == "SOUTH":
                player.setDirection("EAST")
            elif player.getDirection() == "WEST":
                player.setDirection("SOUTH")
            elif player.getDirection() == "NORTH":
                player.setDirection("WEST")
            else:
                print("ERROR")
        elif move == "F":                             # if player chooses to move forward of current position/direction
            if player.getDirection() == "EAST":
                player.moveRight()
            elif player.getDirection() == "SOUTH":
                player.moveDown()
            elif player.getDirection() == "WEST":
                player.moveLeft()
            elif player.getDirection() == "NORTH":
                player.moveUp()
            else:
                print("ERROR")
        elif move == "S":                             # if player chooses to shoot from their current posiiton/direction
            if player.getAmmo() > 0:
                player.setAmmo(player.getAmmo() - 1)  # use arrow
                if player.getDirection() == "EAST":         # if facing east
                    shooting = True
                    origX = player.getX()
                    origY = player.getY()
                    while shooting:                         # checks each continous block for wumpus or wall
                        if theMap.HitWumpus(origX, origY):  # if wumpus hit
                            theMap.RemoveWumpus()
                            shooting = False
                            print("~Screech~")
                            print("Wumpus was killed!!")
                        elif theMap.HitWall(origX, origY):  # if wall hit
                            shooting = False
                            print("~DING~")
                            print("Arrow hit a wall!")
                        else:                               # if nothing hit
                            origY = origY + 1
                elif player.getDirection() == "SOUTH":      # if facing south
                    shooting = True
                    origX = player.getX()
                    origY = player.getY()
                    while shooting:                         # checks each continous block for wumpus or wall
                        if theMap.HitWumpus(origX, origY):  # if wumpus hit
                            theMap.RemoveWumpus()
                            shooting = False
                            print("~Screech~")
                            print("Wumpus was killed!!")
                        elif theMap.HitWall(origX, origY):  # if wall hit
                            shooting = False
                            print("~DING~")
                            print("Arrow hit a wall!")
                        else:                               # if nothing hit
                            origY = origY + 1
                elif player.getDirection() == "WEST":       # if facing west
                    shooting = True
                    origX = player.getX()
                    origY = player.getY()
                    while shooting:                         # checks each continous block for wumpus or wall
                        if theMap.HitWumpus(origX, origY):  # if wumpus hit
                            theMap.RemoveWumpus()
                            shooting = False
                            print("~Screech~")
                            print("Wumpus was killed!!")
                        elif theMap.HitWall(origX, origY):  # if wall hit
                            shooting = False
                            print("~DING~")
                            print("Arrow hit a wall!")
                        else:                               # if nothing hit
                            origY = origY - 1
                elif player.getDirection() == "NORTH":      # if facing north
                    shooting = True
                    origX = player.getX()
                    origY = player.getY()
                    while shooting:                         # checks each continous block for wumpus
                        if theMap.HitWumpus(origX, origY):  # if wumpus hit
                            theMap.RemoveWumpus()
                            shooting = False
                            print("~Screech~")
                            print("Wumpus was killed!!")
                        elif theMap.HitWall(origX, origY):  # if wall hit
                            shooting = False
                            print("~DING~")
                            print("Arrow hit a wall!")
                        else:                               # if nothing hit
                            origX = origX - 1
                else:                                       # should ever get here tbh
                    print("ERROR")
            else:                                           # if player tries to shoot with no ammo
                print("You have no arrows to shoot! ")
        theMap.BoardUpdate(player)                          # update board for next turn

    if player.getDead():                                    # after while loop check to see if player died
        PrintDied()

    elif theMap.HasPlayerWon(player):                       # if not died, check if they won
        PrintWon()


main()