# CONSTANTS
WALL = 0
WALL2 = 5

#Class
class Player:
    # ---------------------------------------Constructor-----------------------------------------
    # PRE: needs to be called
    # POST: instantiate an object
    # PURPOSE: to create an player object to be used in whatever the programmer wants
    MoveList = list()
    def __init__(self, name, x, y, ammo):
        # Private Data Members
        self.__name = name
        self.__y = y                    # x coordinate
        self.__x = x                    # y coordinate
        self.__PrevX = x                # previous x coordinate
        self.__PrevY = y                # previous y coordinate
        self.__ammo = ammo
        self.__pitWarning = False
        self.__wumpWarning = False
        self.__direction = "EAST"
        self.__dead = False
        self.__AtWall = False
        self.__Hint = ""                # hold hints for player
        self.__PrevLocations = set()    # hold previous locations for player
        self.__turns = 0                # hold turn player is on

    # ---------------------------------------GETS-----------------------------------------
    # PRE: needs to be called
    # POST: return PDM
    # PURPOSE: to allow safe access to PDM to other classes or programs
    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def getPrevX(self):
        return self.__PrevX
    def getPrevY(self):
        return self.__PrevY
    def getName(self):
        return self.__name
    def getAmmo(self):
        return self.__ammo
    def getDirection(self):
        return self.__direction
    def getPitWarning(self):
        return self.__pitWarning
    def getDead(self):
        return self.__dead
    def getWumWarning(self):
        return self.__wumpWarning
    def getPrevLocations(self):
        return self.__PrevLocations
    def GetHint(self):
        return self.__Hint

    # ---------------------------------------SETS-----------------------------------------
    # PRE: needs to be called
    # POST: change PDM
    # PURPOSE: to allow changes to PDMs to other classes or programs
    def setDead(self, status):
        self.__dead = status
    def setDirection(self, direction):
        self.__direction = str(direction)
    def setPitWarning(self, warning):
        self.__pitWarning = warning
    def setWumWarning(self, warning):
        self.__wumpWarning = warning
    def setAtWall(self, status):
        self.__AtWall = status
    def setAmmo(self, ammo):
        self.__ammo = ammo
    def setHint(self, hint):
        self.__Hint = hint
    # ---------------------------------------MOVEMENT-----------------------------------------
    # PRE: needs to be called
    # POST: move player
    # PURPOSE: To allow easier movement of the player on a board
    def moveRight(self):
        pair = (self.__x, self.__y)
        self.__PrevLocations.add(pair)      # add to previous moves
        if self.__y + 1 != WALL and self.__y + 1 != WALL2:
            self.__PrevX = self.__x         # save last move
            self.__PrevY = self.__y         # next move
            self.__y = self.__y + 1
        else:
            print("Can't move forward, there is a wall!")

    def moveLeft(self):
        pair = (self.__x, self.__y)
        self.__PrevLocations.add(pair)      # add to previous moves
        if self.__y -1 != WALL and self.__y - 1 != WALL2:
            self.__PrevX = self.__x         # save last move
            self.__PrevY = self.__y
            self.__y = self.__y - 1         # next move
        else:
            print("Can't move forward, there is a wall!")

    def moveDown(self):
        pair = (self.__x, self.__y)
        self.__PrevLocations.add(pair)      # add to previous moves
        if self.__x + 1 != WALL and self.__x + 1 != WALL2:
            self.__PrevX = self.__x         # save last move
            self.__PrevY = self.__y         # next move
            self.__x = self.__x + 1
        else:
            print("Can't move forward, there is a wall!")

    def moveUp(self):
        pair = (self.__x, self.__y)
        self.__PrevLocations.add(pair)      # add to previous moves
        if self.__x - 1 != WALL and self.__x - 1 != WALL2:
            self.__PrevX = self.__x         # save last move
            self.__PrevY = self.__y         # next move
            self.__x = self.__x - 1
        else:
            print("Can't move forward, there is a wall!")

    # -------------------------------Print Update for User-------------------------------------------------
    # PRE: to be called
    # POST: prints knowledge base to txt file and to screen for user's next turn
    # PURPOSE: to keep a record of the knowledge base and tell user their progress
    def PrintKnowledge(self):
        if self.__turns == 0:
            fileWriter = open("KnowledgeBase.txt", "w")  # open file
            self.__turns += 1
            fileWriter.write("V == FOR ALL SYMBOL")
            fileWriter.write("\n3 == THERE EXISTS")
        else:
            fileWriter = open("KnowledgeBase.txt", "a")     # open file
            self.__turns += 1
        fileWriter.write("\nTurn: " + str(self.__turns) + "\n")
        if self.__AtWall:                               # if at wall
            strWall = "BUMP!!! You hit a wall!"
            strWallFOL = "Vx,y Wall(y) -> 3x Adjacent(Human(x),y)"
            print(strWall)                              # print to screen
            fileWriter.write(strWall)                   # write to knowledge base
            fileWriter.write("\n")
            fileWriter.write(strWallFOL)
            fileWriter.write("\n")
            self.setAtWall(False)  # reset PDM
        basic = ("You are in room [" + str(self.__y) + " " + str(self.__x) + "] of the cave. Facing " + self.__direction)
        basicFOL = "Vx -> 3x Location(Human(x))"
        print(basic)                                    # print to screen
        fileWriter.write(basic)                         # write to knowledge base
        fileWriter.write("\n")
        fileWriter.write(basicFOL)
        fileWriter.write("\n")
        if self.__wumpWarning:                          # if wumpus is near
            wumpWarning = "There is a STENCH in here!"
            wumpWarningFOL = "Vx,y Location(Human(x)) ^ Stench(y)-> Smells(Human(x)) => Vx,y Wumpus(y) ->  NextTo(Human(x),y) ^ Stench(y)"
            print(wumpWarning)                          # print to screen
            fileWriter.write(wumpWarning)               # write to knowledge base
            fileWriter.write("\n")
            fileWriter.write(wumpWarningFOL)
            fileWriter.write("\n")
            self.setWumWarning(False)                   # reset PDM
        if self.__pitWarning:                           # if pit is near
            pitWarning = "There is a BREEZE in here!"
            pitWarningFOL = "Vx,y Location(Human(x)) ^ Breeze(y)-> Cold(Human(x)) => Vx,y Pit(y) ->  NextTo(Human(x),y) ^ Breeze(y)"
            print(pitWarning)                           # print to screen
            fileWriter.write(pitWarning)                # write to knowledge base
            fileWriter.write(" ")
            fileWriter.write(pitWarningFOL)
            fileWriter.write("\n")
            self.setPitWarning(False)                   # reset PDM
        if self.__Hint != "" and self.__Hint != "\n":   # if there is a hint
            fileWriter.write(self.__Hint)               # write hint to knowledge base
            HintFOL = "Vx,y,z,w Locations(x,y,z,w) -> 3x,y,z,w Pit/Wumpus(x) || Pit/Wumpus (y) || Pit/Wumpus(z) || Pit/Wumpus(w)"
            fileWriter.write("\n")
            fileWriter.write(HintFOL)
            fileWriter.write("\n")
            print(self.__Hint)                          # print to screen
            self.__Hint = ""                            # reset hint
        fileWriter.write("\n")                          # end file with a newline
        fileWriter.close()                              # close file
