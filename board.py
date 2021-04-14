# IMPORTS
import math

# Constants
WUMPUS = "W"
WUMPUS_WARNING = "S"
PIT = "P"
PIT_WARNING = "B"
GOLD = "G"
HUMAN = "H"
WALL = 0
WALL2 = 5
WEST_WALL = 0
EAST_WALL = 5
NORTH_WALL = 0
SOUTH_WALL = 5

#CLASS
class Board:
    # ---------------------------------------Constructor------------------------------
    # PRE: needs to be called with values
    # POST:  instantiates the board with values and creates board object
    # PURPOSE: to create the board with correct values
    def __int__(self, values):
        self.__board = self.adjustBoard(self.createBoard(values))  # create board / add obstacles / save board
        #self.PrintBoard()

    # --------------------------------------------------------------------------------
    # PRE: needs values to create the board and assumed it will be called in constructor
    # POST: creates the board with proper values
    # PURPOSE: to give a visual representation of the playing field
    def createBoard(self, values):
        size = int(math.sqrt(len(values)))                          # basically size of any one row/column
        rows = size
        cols = size
        theMap = [[0 for row in range(rows + 2)] for col in range(cols + 2)]    # sets entire board to 0
        count = 0
        for row in range(1, size + 1):                                          # for each row
            for col in range(1, size + 1):                                      # for each column
                theMap[row][col] = values[count]                                # place value in board
                count += 1
        return theMap

    # --------------------------------------------------------------------------------
    # PRE: needs the board it is going to change
    # POST: updates the board with obstacles
    # PURPOSE: To create an updated board with obstacles
    def adjustBoard(self, board):
        size = int(len(board))                                                  # basically size of a row/column
        rows = size
        cols = size
        count = 0
        for row in range(1, size - 1):                         # 1 to size -1 because the border needs to be left as 0's
            for col in range(1, size - 1):
                if board[row][col] == WUMPUS:   # fill in areas with a pit with surrounding pit warnings
                    if row-1 != SOUTH_WALL and board[row][col] != PIT and board[row-1][col] == "X": board[row-1][col] = "S"
                    elif row-1 != SOUTH_WALL and board[row][col] != PIT and board[row-1][col] != "X": board[row-1][col] = str(board[row-1][col]) + "S"
                    if row+1 != NORTH_WALL and board[row][col] != PIT and board[row+1][col] == "X": board[row+1][col] = "S"
                    elif row+1 != NORTH_WALL and board[row][col] != PIT and board[row+1][col] != "X": board[row+1][col] = str(board[row+1][col]) + "S"
                    if col-1 != WEST_WALL and board[row][col] != PIT and board[row][col-1] == "X": board[row][col-1] = "S"
                    elif col-1 != WEST_WALL and board[row][col] != PIT and board[row][col-1] != "X": board[row][col-1] = str(board[row][col-1]) + "S"
                    if col+1 != EAST_WALL and board[row][col] != PIT and board[row][col+1] == "X": board[row][col+1] = "S"
                    elif col+1 != EAST_WALL and board[row][col] != PIT and board[row][col+1] != "X": board[row][col+1] = str(board[row][col+1]) + "S"
                elif board[row][col] == PIT:    # fill in areas with a wumpus with surrounding wumpus warnings
                    if row-1 != NORTH_WALL and board[row][col] != WUMPUS and board[row-1][col] == "X": board[row-1][col] = "B"
                    elif row-1 != NORTH_WALL and board[row][col] != WUMPUS and board[row-1][col] != "X" and board[row-1][col] != "B": board[row-1][col] = str(board[row-1][col]) + "B"
                    if row+1 != SOUTH_WALL and board[row][col] != WUMPUS and board[row+1][col] == "X":board[row+1][col] = "B"
                    elif row+1 != SOUTH_WALL and board[row][col] != WUMPUS and board[row+1][col] != "X" and board[row+1][col] != "B": board[row+1][col] = str(board[row+1][col]) + "B"
                    if col-1 != WEST_WALL and board[row][col] != WUMPUS and board[row][col-1] == "X":board[row][col-1] = "B"
                    elif col-1 != WEST_WALL and board[row][col] != WUMPUS and board[row][col-1] != "X" and board[row][col-1]: board[row][col-1] = str(board[row][col-1]) + "B"
                    if col+1 != EAST_WALL and board[row][col] != WUMPUS and board[row][col+1] == "X":board[row][col+1] = "B"
                    elif col+1 != EAST_WALL and board[row][col] != WUMPUS and board[row][col+1] != "X" and board[row][col+1] != "B" : board[row][col+1] = str(board[row][col+1]) + "B"
                count += 1
        return board
    # --------------------------------------------------------------------------------
    # PRE: to be called
    # POST: prints board
    # PURPOSE: shows a visual representation of the board
    def PrintBoard(self):
        for row in range(len(self.__board)):
            print()     # different ifs have different spacing based on # of characters in that spot
            for col in range(len(self.__board)):
                if len(str(self.__board[row][col])) == 3:
                    print((str(self.__board[row][col]) + " "), end="")
                elif len(str(self.__board[row][col])) == 2:
                    print((str(self.__board[row][col]) + "  "), end="")
                elif len(str(self.__board[row][col])) == 1 and self.__board[row][col] != 0:
                    print((str(self.__board[row][col]) + "   "), end="")
                else:
                    print("-" + "   ", end="")

    # --------------------------------------------------------------------------------
    # PRE: to be called with player, assumes to be called from board update
    # POST: centralizes major updates throughout the board for the player
    # PURPOSE: to determines player's warnings and give advice to player
    def BoardUpdate(self, player):
        self.HasPlayerHitWall(player)   # check if player hit a wall
        self.isPlayerNearWum(player)    # check if player is near a wumpus
        self.isPlayerNearPit(player)    # check if player is near a pit
        self.isPlayerDead(player)       # check if player is ndead
        self.GetHint(player)            # check for hints to give
        self.UpdateHuman(player)        # update human location on map (cosmetic)
        self.PrintBoard()               # print the board (cosmetic)
        print()
        # ---------------------------------------GETS-----------------------------------------
        # PRE: to be called with player, assumes to be called from board update
        # POST: sets the player's boolean to won if player wins the game
        # PURPOSE: to determine if the player has won

    def UpdateHuman(self, player):
        # if player isn't in current spot update it to be there
        if HUMAN not in str(self.__board[player.getX()][player.getY()]):
            self.__board[player.getX()][player.getY()] = str(self.__board[player.getX()][player.getY()]) + "H"
        # if player's previous spot doesn't equal current spot erase it
        if player.getX() != player.getPrevX() or player.getY() != player.getPrevY():
            self.__board[player.getPrevX()][player.getPrevY()] = str(self.__board[player.getPrevX()][player.getPrevY()]).replace("H", "")
    # ---------------------------------------GETS-----------------------------------------
    # PRE: to be called with player, assumes to be called from board update
    # POST: sets the player's boolean to won if player wins the game
    # PURPOSE: to determine if the player has won
    def HasPlayerWon(self, player):
        x = player.getX()
        y = player.getY()
        # if player locations matches gold then true
        if GOLD in str(self.__board[player.getX()][player.getY()]):
            return True
        else:
            return False
    # --------------------------------------------------------------------------------
    # PRE: to be called with player, assumes to be called from board update
    # POST: sets the player's boolean to dead if player is no longer alive
    # PURPOSE: to determine if the player is still alive
    def isPlayerDead(self, player):
        # if player in the same location as a pit or the wumpus then they are dead
        if WUMPUS in str(self.__board[player.getX()][player.getY()]) or PIT in str(self.__board[player.getX()][player.getY()]):
            player.setDead(True)

    # --------------------------------------------------------------------------------
    # PRE: to be called with player, assumes to be called from board update
    # POST: sets the player's boolean to warning if player is near wumpus
    # PURPOSE: to determine if the player is near the wumpus
    def isPlayerNearWum(self, player):
        # if player is in the same location as a wumpus warning then they are in danger
        if WUMPUS_WARNING in str(self.__board[player.getX()][player.getY()]):
            player.setWumWarning(True)
    # --------------------------------------------------------------------------------
    # PRE: to be called with player, assumes to be called from board update
    # POST: sets the player's boolean to warning if near a pit
    # PURPOSE: to determine if the player is near a pit
    def isPlayerNearPit(self, player):
        # if player is in the same locations as a pit warning then they are in danger
        if PIT_WARNING in str(self.__board[player.getX()][player.getY()]):
            player.setPitWarning(True)

    # --------------------------------------------------------------------------------
    # PRE: to be called with player, assumes to be called from board update
    # POST: sees if player hit a wall when moving around the map
    # PURPOSE: to determine if a player has hit a wall
    def HasPlayerHitWall(self, player):
        if player.getDirection() == "EAST":
            x = player.getY() + 1
            y = player.getX()
            if self.__board[x][y] == WALL:          # if wall in front of them
                player.setAtWall(True)
        elif player.getDirection() == "NORTH":
            x = player.getX() - 1
            y = player.getY()
            if self.__board[x][y] == WALL:          # if wall in front of them
                player.setAtWall(True)
        elif player.getDirection() == "WEST":
            x = player.getX()
            y = player.getY() - 1
            if self.__board[x][y] == WALL:          # if wall in front of them
                player.setAtWall(True)
        elif player.getDirection() == "SOUTH":
            x = player.getX() + 1
            y = player.getY()
            if self.__board[x][y] == WALL:          # if wall in front of them
                player.setAtWall(True)
        else: # should never get here
            print("ERROR")

    # --------------------------------------------------------------------------------
    # PRE: needs coordinates
    # POST: return if coordinates match Wumpus
    # PURPOSE: returns if coordinates are where the wumpus is
    def HitWumpus(self, x, y):
        # if location is where the wumpus is then true
        if self.__board[x][y] == WUMPUS:
            return True
        else:
            return False
    # --------------------------------------------------------------------------------
    # PRE: needs coordinates
    # POST: return if coordinates match a wall
    # PURPOSE: returns if coordinates is where a wall is
    def HitWall(self, x, y):
        # if location is where a wall is then true
        if self.__board[x][y] == WALL:
            return True
        else:
            return False
    # --------------------------------------------------------------------------------
    # PRE: assumes wumpus has been hit by an arrow
    # POST: removes wumpus from board
    # PURPOSE: if wumpus has been shot, it needs to be removed from the board
    def RemoveWumpus(self):
        size = int(len(self.__board))
        rows = size
        cols = size
        # goes through each block looking for wumpus or wumpus warning
        for row in range(1, size - 1):
            for col in range(1, size - 1):
                # if wumpus warning or wumpus, replace with x
                if self.__board[row][col] == WUMPUS or self.__board[row][col] == WUMPUS_WARNING: self.__board[row][col] = "X"
                # if wumpus warning has other characters in block get rid of warning
                if WUMPUS_WARNING in str(self.__board[row][col]): self.__board[row][col] = str(self.__board[row][col]).replace("S", "")
                # if wumpus has other characters in block get rid of wumpus
                if WUMPUS in str(self.__board[row][col]): self.__board[row][col] = str(self.__board[row][col]).replace("W", "")
    # --------------------------------------------------------------------------------
    # PRE: needs player and to be called
    # POST: determines hints based on player's coords
    # PURPOSE: to gather information about the player's surrounds so hint can be given
    def GetHint(self, player):
        hint = ""
        # if player has a pit warning (breeze)
        if player.getPitWarning():
            hint = "There is a PIT in one or more of these locations: "
            # produce the four possible hints
            pair = (player.getX() + 1, player.getY())
            pair2 = (player.getX() - 1, player.getY())
            pair3 = (player.getX(), player.getY() + 1)
            pair4 = (player.getX(), player.getY() - 1)
            # remove previous locations from hints and if locations are invalid
            if pair not in player.getPrevLocations() and pair[1] != WALL and pair[0] != WALL and pair[1] != WALL2 and pair[0] != WALL2:
                hint = hint + "[" + str(pair[1]) + "," + str(pair[0]) + "]"
            if pair2 not in player.getPrevLocations()and pair2[1] != WALL and pair2[0] != WALL and pair2[1] != WALL2 and pair2[0] != WALL2:
                hint = hint + "[" + str(pair2[1]) + "," + str(pair2[0]) + "]"
            if pair3 not in player.getPrevLocations()and pair3[1] != WALL and pair3[0] != WALL and pair3[1] != WALL2 and pair3[0] != WALL2:
                hint = hint + "[" + str(pair3[1]) + "," + str(pair3[0]) + "]"
            if pair4 not in player.getPrevLocations()and pair4[1] != WALL and pair4[0] != WALL and pair4[1] != WALL2 and pair4[0] != WALL2:
                hint = hint + "[" + str(pair4[1]) + "," + str(pair4[0]) + "]"
        # if player has a wumpus warning (stench)
        if player.getWumWarning():
            hint = "There is a WUMPUS in one of these locations: "
            # produce four possible hints
            pair = (player.getX() + 1, player.getY())
            pair2 = (player.getX() - 1, player.getY())
            pair3 = (player.getX(), player.getY() + 1)
            pair4 = (player.getX(), player.getY() - 1)
            # remove previous locations from hints and if locations are invalid
            if pair not in player.getPrevLocations() and pair[1] != WALL and pair[0] != WALL and pair[1] != WALL2 and pair[0] != WALL2:
                hint = hint + "[" + str(pair[1]) + "," + str(pair[0]) + "]"
            if pair2 not in player.getPrevLocations() and pair2[1] != WALL and pair2[0] != WALL and pair2[1] != WALL2 and pair2[0] != WALL2:
                hint = hint + "[" + str(pair2[1]) + "," + str(pair2[0]) + "]"
            if pair3 not in player.getPrevLocations() and pair3[1] != WALL and pair3[0] != WALL and pair3[1] != WALL2 and pair3[0] != WALL2:
                hint = hint + "[" + str(pair3[1]) + "," + str(pair3[0]) + "]"
            if pair4 not in player.getPrevLocations() and pair4[1] != WALL and pair4[0] != WALL and pair4[1] != WALL2 and pair4[0] != WALL2:
                hint = hint + "[" + str(pair4[1]) + "," + str(pair4[0]) + "]"
        # add newline to hint
        hint = hint + "\n"
        player.setHint(hint)
