import pygame
import random
import math
import os
import neat
import pickle
import time
import numpy as np


pygame.init()



global Car_List
Car_List = [] # List with all Car-Objects


#-----Colors------#
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0,0,255)
green = (0,255,0)
black = (0,0,0)
yellow = (255, 255, 0)

font = pygame.font.Font(None, 80)
fontStats = pygame.font.Font(None, 30)


#-----Lines------#
line_width = 4
row_height = 50 + line_width
row_width = 50 + line_width


#-----Level------#
global level,level_Indices
level = []
level_Indices = [0]
Number_Of_Fields_x = 20
Number_Of_Fields_y = 15
Window_Width = row_height * Number_Of_Fields_x + line_width
Window_Height = row_width * Number_Of_Fields_y + line_width
Level_Offset_Y = 0 # Y-Offset of Level (Level is constantly moving upwards) 
Level_Speed = -1# Speed by which the level moves upwards in pixels

#-----Window------#
window = pygame.display.set_mode((Window_Width,Window_Height))
pygame.display.set_caption('DZT_Spiel')

# Each generation will run through [NumLevels] levels. Based on how many checkpoints a player reached, he will be rewarded
# By generating many levels, players who make the right moves by accident will not be preffered
# ------------------------------------------------------------------------------------------------------------------------ #
NumLevels = 1 # Number of Levels that each generation will play
LevelLength = 100 # Length / Number of fields that each level contains
AllLevels = [] # Lists all Level-Lists, containing "grass" or "street"
AllDirections = [] # Lists all Lists that contain the direction of the Cars for each street
AllOffsets = [] # Lists all lists that contain the x-offset of the Cars for each street 
RewardLevels = [] # If a player reaches a level which is in this list, he will get a reward 

# Generating All the different Levels
for i in range(NumLevels): # iterate through every level
    
    CurrentLevel = []
    CurrentDirections = []
    CurrentOffsets = []

    while len(CurrentLevel)<LevelLength: # add new level rows until LevelLength is reached


        NumberOfGrassRows = random.choice([2,3,4])
        NumberOfStreetRows = 1

        for j in range(NumberOfGrassRows): # add grass rows to CurrentLevel
            
            CurrentLevel.append("grass") # add a single grass row
            CurrentDirections.append(0) # input does not matter since grass-rows have no Cars
            CurrentOffsets.append(0) # input does not matter since grass-rows have no Cars
            
        for j in range(NumberOfStreetRows): # add street rows to CurrentLevel (For-loop only for future use of multiple-lnae-streets)
            
            CurrentLevel.append("street") # add a single street row

            # generate random Car direction and x-offset for the start of the level
            Direction = random.choice([-1,1])
            Offset = random.random()*2

            # Store Car directions and x-offsets
            CurrentDirections.append(Direction)
            CurrentOffsets.append(Offset)

    while len(CurrentLevel)>LevelLength: # remove last row until LevelLength is reached, in case the random generation added too many rows
        CurrentLevel.pop(-1)

    # Store all Level information for current level 
    AllLevels.append(CurrentLevel)
    AllDirections.append(CurrentDirections)
    AllOffsets.append(CurrentOffsets)

# Player Should be rewarded for reaching every fifth row
for i in range(5,LevelLength + 1,5):
    RewardLevels.append(i)





def generateLevel():
    # generates all layers for the level --> Grass- and Street-Layers

    generateGrass()
    generateStreet() 

    if len(level)<3*Number_Of_Fields_y: # add further levels if levels are running out
        generateLevel()

def generateGrass(Number_Of_Rows = None):
    # generates a random number of grass layers and adds them to the level 

    if Number_Of_Rows == None:
        Number_Of_Rows = random.choice([2, 3])

    for i in range(Number_Of_Rows):
        level.append("grass")
        level_Indices.append(level_Indices[-1] + 1) # add next indice with indice-number increased by one 

def generateStreet(Number_Of_Rows = None,RoadDifficulty = None,x_disposition = None,direction = None):
    # generates street layers and adds them to the level 

    if Number_Of_Rows == None:
        Number_Of_Rows = random.choice([1, 2, 3])
    if RoadDifficulty == None:
        RoadDifficulty = random.choice([1, 2, 3])
    if x_disposition == None:
        x_disposition = random.choice([0, 0.4, 0.8, 1.2, 1.6, 2])
    if direction == None:
        direction = random.choice([1, -1])
    
    #Number_Of_Rows = 1
    for i in range(Number_Of_Rows):
        level.append("street")
        level_Indices.append(level_Indices[-1] + 1) # add next indice with indice-number increased by one 

    RoadDifficulty = 1 # set RoadDifficulty to easy for testing purposes  

    # Change CarSpeed and SpaceBetweenCars according to RoadDifficulty
    if RoadDifficulty == 1:
        SpaceBetweenCars = 2.5
        CarSpeed = 1
    elif RoadDifficulty == 2:
        SpaceBetweenCars = 4
        CarSpeed = 1.5
    elif RoadDifficulty == 3:
        SpaceBetweenCars = 3.5
        CarSpeed = 1

    # Calculate Number of Cars in each Row
    NumCars = math.ceil(Number_Of_Fields_x/(2 + SpaceBetweenCars))

    Field_Pos_Y = level_Indices[-1] - Number_Of_Rows + 1

    # Add Cars for each street row
    for i in range(Number_Of_Rows):
        
        Field_Pos_X = 1
        
        
        for j in range(NumCars):
            
            # create Car and set speed and direction
            currentCar = Car(Field_Pos_X + x_disposition,Field_Pos_Y)
            currentCar.direction = direction
            currentCar.speed = CarSpeed

            # calculate X-position of next Car 
            CarFieldWidth = 2
            Field_Pos_X = Field_Pos_X + CarFieldWidth + SpaceBetweenCars

        Field_Pos_Y = Field_Pos_Y + 1

def moveLevel(player):
    # moves Level up, so that player is forced to constantly move down

    global Level_Offset_Y
    
    Max_Row = 8 # If player is moving faster than the level, i.e. he crosses the 8th Row on the screen, the level moves faster

    if Level_Speed < -player.speed_y*row_height or player.y + Level_Offset_Y < Max_Row*row_height:
        # Normal Level speed

        Level_Offset_Y = Level_Offset_Y + Level_Speed

    else:
        # Higher speed if player is faster than the level

        Level_Offset_Y = Level_Offset_Y - player.speed_y*row_height


def draw_level():
    # draws every level

    for i in range(len(level)):

        if level[i] == "grass":
            currentColor = green
        else:
            currentColor = black
        

        pygame.draw.rect(window,currentColor,(0,Level_Offset_Y + (level_Indices[i] - 1) * row_height,Window_Width,2*row_height))
        

def draw_number(number, x, y):
    text = font.render(str(number), True, black)
    window.blit(text, (x, y))

def drawStats(FirstArgument,SecondArgument,Fitness):
    # draws three different number values in the top right corner of the screen
    # useful for analysing progress during simulation

    # White square backgorung
    pygame.draw.rect(window,white,(Window_Width-250,0,250,100))
    
    # First Number
    text = fontStats.render(f"1stArg: {FirstArgument}", True, black)
    window.blit(text, (Window_Width-240, 10))
    
    # Second Number
    text = fontStats.render(f"2ndArg: {SecondArgument}", True, black)
    window.blit(text, (Window_Width-240, 40))
    
    # Third Number
    text = fontStats.render(f"Fitness: {Fitness}", True, black)
    window.blit(text, (Window_Width-240, 70))
    


# Functions to handle the second coordinate system
# converts pixel coordinates in Field coordinates and vice versa
def calc_Field_Pos_From_Pos(Pos_x,Pos_y):
    Field_pos_x = (Pos_x - line_width)/row_width + 1
    Field_pos_y = (Pos_y - line_width)/row_height + 1
    return (Field_pos_x,Field_pos_y)

def calc_Field_Pos_From_Pos_X(Pos_x):
    (Field_pos_x,Field_pos_y) = calc_Field_Pos_From_Pos(Pos_x,0)
    return Field_pos_x

def calc_Field_Pos_From_Pos_Y(Pos_y):
    (Field_pos_x,Field_pos_y) = calc_Field_Pos_From_Pos(0,Pos_y)
    return Field_pos_y

def calc_Pos_From_Field_Pos(Field_pos_x,Field_pos_y):
    Pos_x = line_width + (Field_pos_x-1) * row_width
    Pos_y = line_width + (Field_pos_y-1) * row_width
    return (Pos_x,Pos_y)

def calc_Pos_From_Field_Pos_X(Field_pos_x):
    (Pos_x,Pos_y) = calc_Pos_From_Field_Pos(Field_pos_x,0)
    return Pos_x

def calc_Pos_From_Field_Pos_Y(Field_pos_y):
    (Pos_x,Pos_y) = calc_Pos_From_Field_Pos(0,Field_pos_y)
    return Pos_y



def drawGrid():
    # draws grid lines to seperate fields

    for i in range(Number_Of_Fields_x+1):
        pygame.draw.rect(window, blue,((i) * row_width,0,line_width,Window_Height))
 
    for i in range(len(level_Indices)):
        pygame.draw.rect(window, blue,(0,(level_Indices[i] - 1)* row_height + Level_Offset_Y,Window_Width,line_width))

    

def WindowFlip():
    # draws everything onto the window that was drawn since last WindowFlip
    pygame.display.flip()


def draw_everything():
    # draws the level and all cars, but not the player

    window.fill(white)
    draw_level()
    drawGrid()
    Car.drawAllCars()
    
def find_intersect(a1, b1, a2, b2):
    """
    Finds the intersection point of two vector lines (2D) or prints if there is none.

    Parameters:
    a1, b1: Support vector and direction vector of first vector line 
    a2, b2: Support vector and direction vector of second vector line
    """

    # convert arrays into numpy arrays
    a1 = np.array(a1)
    b1 = np.array(b1)
    a2 = np.array(a2)
    b2 = np.array(b2)

    # Equation intersection: a1 + t*b1 = a2 + s*b2  =>  t*b1 - s*b2 = a2 - a1
    
    # Create coefficient matrix for the left side of the equation
    A = np.column_stack((b1, -b2))
    # Right side of the equation
    rhs = a2 - a1

    try:
        # Solving the linear equation
        t_s = np.linalg.solve(A, rhs)
        t, s = t_s
        return [s,t]
    
    except np.linalg.LinAlgError:
        # In case no intersect was found, return None
        return None



class Player:
    
    Width = row_width -  line_width
    Height = row_height - line_width
    speed_x = 0
    speed_y = 0
    Normal_Player_Speed = 1/10 # Blocks per Frame; must be between 0 and  1 
    score = 0
    color = red
    
    # Simulates Keypresses for bots or AI's
    KeyPressedLeft = False
    KeyPressedRight = False
    KeyPressedUp = False
    KeyPressedDown = False

    def __init__(self, FieldPos_x, FieldPos_y):

        # Position in Field-coordinate system is set
        self.FieldPos_x = FieldPos_x
        self.FieldPos_y = FieldPos_y

        # convert field coordinates into pixel coordinates
        self.x , self.y = calc_Pos_From_Field_Pos(FieldPos_x,FieldPos_y)

        self.time = 0 # increased by one for every clock tick
        self.stop = False # set to true when player collides with car or level window borders

        self.survivedTimes = 0
        self.reachedLevels = []
        self.crossedLevelThreshold = 0
    
    def move(self):
        # moves player
        self.updatePlayerSpeed()
        self.x = self.x + self.speed_x * row_height
        self.y = self.y + self.speed_y * row_height
        
        
    def draw(self):
        # draws player
        pygame.draw.rect(window, self.color, (self.x,self.y + Level_Offset_Y,self.Width,self.Height))

    def is_moving(self):
        # returns True if player is moving
        return self.speed_x != 0 or self.speed_y != 0 

    # function for reacting to keyboard inputs
    '''def React_To_Keypressed(self,keys):
        if self.is_moving() == False:
            if keys[pygame.K_DOWN]:
                self.speed_y = self.Normal_Player_Speed
            elif keys[pygame.K_UP]:
                self.speed_y = -self.Normal_Player_Speed 
            elif keys[pygame.K_RIGHT]:
                self.speed_x = self.Normal_Player_Speed 
            elif keys[pygame.K_LEFT]:
                self.speed_x = -self.Normal_Player_Speed'''

    def React_To_Keypressed(self):
        # sets player speed according to simulated keypresses

        if self.is_moving() == False:
            if self.KeyPressedDown:
                self.speed_y = self.Normal_Player_Speed
            elif self.KeyPressedUp:
                self.speed_y = -self.Normal_Player_Speed 
            elif self.KeyPressedRight:
                self.speed_x = self.Normal_Player_Speed 
            elif self.KeyPressedLeft:
                self.speed_x = -self.Normal_Player_Speed

    def updatePlayerSpeed(self):
        # resets current keypresses
        # makes sure that player movement stops when a new Field is reached
        # so that pressing a key once, causes the player to move only one field

        self.KeyPressedDown = False
        self.KeyPressedUp = False
        self.KeyPressedRight = False
        self.KeyPressedLeft = False


        # When the player moves, the Field coordinate is only updated once a new field is reached
        # By checking if the current pixel position is more than one Field away from the initial Field position, 
        # we can tell if the player moved one block
        # Then the pixel position of the player is set to the exact Fieldposition the player moved to, in 
        # order to avoid that the player move a few pixels too far
        # The Fieldposition of the player is then updated and the speed is set to zero
        if self.speed_y>0: # If player is moving down
            if self.y + self.speed_y * row_height > calc_Pos_From_Field_Pos_Y(self.FieldPos_y+1):
                self.speed_y = 0
                self.FieldPos_y = self.FieldPos_y + 1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
        
        elif self.speed_y<0: # If player is moving up
            if self.y + self.speed_y * row_height < calc_Pos_From_Field_Pos_Y(self.FieldPos_y-1):
                self.speed_y = 0
                self.FieldPos_y = self.FieldPos_y + -1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
        
        if self.speed_x>0: # If player is moving right
            if self.x + self.speed_x * row_width > calc_Pos_From_Field_Pos_X(self.FieldPos_x+1):
                self.speed_x = 0
                self.FieldPos_x = self.FieldPos_x + 1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
        
        elif self.speed_x<0: # If player is moving left
            if self.x + self.speed_x * row_width < calc_Pos_From_Field_Pos_X(self.FieldPos_x-1):
                self.speed_x = 0
                self.FieldPos_x = self.FieldPos_x + -1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
    
    def getScore(self):
        
        # returns the Field number of the highest Field the player ever reached, 
        # even if he went backwards after that
        currentScore = calc_Field_Pos_From_Pos_Y(self.y)
        if self.score<currentScore:
            self.score = currentScore
        return self.score
    
    def getRealScore(self):
        # returns the current pixel position of the player
        currentScore = self.y
        return currentScore

    def drawScore(self):
        # draws player score in the bottom left corner of the window

        rounded_score = math.floor(self.score)
        num_digits = len(str(rounded_score))
        pygame.draw.rect(window,white,(0,Window_Height-row_height,num_digits*row_width,row_height))

        draw_number(rounded_score,10,Window_Height-row_height)


    def check_for_collision(self):
        # check if player is outside of window boundaries
        if self.x<0 or self.y + Level_Offset_Y<0 or self.x + self.Width >= Window_Width or self.y + self.Height + Level_Offset_Y >= Window_Height:
            return True
       

        # check if cars are colliding with player

        Player_Field_Pos_Y = calc_Field_Pos_From_Pos_Y(self.y)
        for i in Car_List:
            Car_Field_Pos_Y = calc_Field_Pos_From_Pos_Y(i.y)
            if Player_Field_Pos_Y +2 < Car_Field_Pos_Y:
                # skip to next car, if car is not in the vicinity of the player
                # saves runtime because not all sides of the car have to be checked for collision
                continue
            #if Player_Field_Pos_Y + 2 > Car_Field_Pos_Y:
            #    break
            # check top left corner of player
            if (self.x >= i.x and self.x <= i.x + i.width) and (self.y  >= i.y and self.y <= i.y + i.height):
                return True
            # check top right corner of player
            if (self.x + self.Width >= i.x and self.x + self.Width <= i.x + i.width) and (self.y >= i.y and self.y <= i.y + i.height):
                return True
            # check bottom left corner of player
            if (self.x >= i.x and self.x <= i.x + i.width) and (self.y  + self.Height >= i.y and self.y  + self.Height <= i.y + i.height):
                return True
            # check bottom right corner of player
            if (self.x + self.Width >= i.x and self.x + self.Width <= i.x + i.width) and (self.y + self.Height >= i.y and self.y + self.Height <= i.y + i.height):
                return True
        
        # If this line is reached, no collisions occured
        return False
            
    def getDistanceForAngle(self,Angle):
            # draws a line beginning from the center of the player
            # Angle is the angle between the positive x-axis and the line (clockwise)
            # The line stops at the first obstacle (either Car or window frame)
            # Returns the length of the line

            
            def DistanceForHorizontalLinesVectorSystem(player_x,player_y,y_line,x_Border_1,x_Border_2):
                # Calculates distance between player and a horizontal line
                # player_x,player_y = center position of player
                # y_line = y-axis intercept of line
                # x_Border_1,x_Border_2 = x-limits for line

                if Angle == 0 or Angle == 180: # distance can not be determined if the Angle is also horizontal
                    return None
                
                # Define vector equation for distance line 
                # Distanceline = SupportVector_Player + s * DirectionVector_Player
                # Length of the direction vector is set to 1
                # If an intercept with a line is calculated, the s-parameter is equal to the distance, 
                # provided s is greater than 0, since a ngeative s would mean, that the intercept is in  the 
                # opposite direction of the Angle
                SupportVector_Player = [player_x,player_y]
                DirectionVector_Player = [math.cos(math.radians(Angle)),math.sin(math.radians(Angle))]

                # Define vector equation for obstacle line 
                # Distanceline = SupportVector_Obstacle + t * DirectionVector_Obstacle
                # Length of the direction vector is set to the distance between x_Border_1 and x_Border_2
                # If an intercept with a line is calculated, the t-parameter must be between 0 and 1, in order to be valid
                SupportVector_Obstacle = [x_Border_1,y_line]
                DirectionVector_Obstacle = [x_Border_2-x_Border_1,0]

                # returns t and s paramters of intercept position            
                (t , s) = find_intersect(SupportVector_Player,DirectionVector_Player,SupportVector_Obstacle,DirectionVector_Obstacle)
                
                if 0 <= t <= 1 and s>=0:
                    return s
                else: 
                    return None 
            
            def DistanceForVerticalLinesVectorSystem(player_x,player_y,x_line,y_Border_1,y_Border_2):
                # Calculates distance between player and a vertical line
                # player_x,player_y = center position of player
                # x_line = x-axis intercept of line
                # y_Border_1,y_Border_2 = y-limits for line

                if Angle == 90 or Angle == 270: # distance can not be determined if the Angle is also vertical
                    return None      

                # Define vector equation for distance line 
                # Distanceline = SupportVector_Player + s * DirectionVector_Player
                # Length of the direction vector is set to 1
                # If an intercept with a line is calculated, the s-parameter is equal to the distance, 
                # provided s is greater than 0, since a ngeative s would mean, that the intercept is in  the 
                # opposite direction of the Angle
                SupportVector_Player = [player_x,player_y]
                DirectionVector_Player = [math.cos(math.radians(Angle)),math.sin(math.radians(Angle))]

                # Define vector equation for obstacle line 
                # Distanceline = SupportVector_Obstacle + t * DirectionVector_Obstacle
                # Length of the direction vector is set to the distance between x_Border_1 and x_Border_2
                # If an intercept with a line is calculated, the t-parameter must be between 0 and 1, in order to be valid
                SupportVector_Obstacle = [x_line,y_Border_1]
                DirectionVector_Obstacle = [0,y_Border_2-y_Border_1]

                # returns t and s paramters of intercept position            
                (t , s) = find_intersect(SupportVector_Player,DirectionVector_Player,SupportVector_Obstacle,DirectionVector_Obstacle)
                
                if 0 <= t <= 1 and s >= 0:
                    return s
                else: 
                    return None 
                


            # x- and y-position of player center
            y = self.y + self.Height/2
            x = self.x + self.Width/2
            y_real = y + Level_Offset_Y # necessary for dealing with window borders


            Distances = [] # Stores all distances between players and obstacle lines

            # Check window borders
            # Top Line
            NextDistance = DistanceForHorizontalLinesVectorSystem(x,y_real,0,0,Window_Width)
            if not NextDistance==None:
                Distances.append(NextDistance)
            # Bottom Line
            NextDistance = DistanceForHorizontalLinesVectorSystem(x,y_real,Window_Height,0,Window_Width)
            if not NextDistance==None:
                Distances.append(NextDistance)
            # Left Line
            NextDistance = DistanceForVerticalLinesVectorSystem(x,y_real,0,0,Window_Height)
            if not NextDistance==None:
                Distances.append(NextDistance)
            # Right Line
            NextDistance = DistanceForVerticalLinesVectorSystem(x,y_real,Window_Width,0,Window_Height)
            if not NextDistance==None:
                Distances.append(NextDistance)


            # Check all Cars
            for Car in Car_List:
                
                # do not check distances, if Cars are not visible in the window
                if Car.y + Car.height + Level_Offset_Y < 0:
                    continue
                if Car.y + Level_Offset_Y > Window_Height:
                    break
                # do not check distances if Car is not in the general direction of the Angle
                if (Angle>0 and Angle<90) and not (x <= Car.x  and y <= Car.y):
                    continue
                if (Angle>90 and Angle<180) and not (x >= Car.x + Car.width  and y <= Car.y):
                    continue
                if (Angle>180 and Angle<270) and not (x >= Car.x + Car.width  and y >= Car.y + Car.height):
                    continue
                if (Angle>270 and Angle<360) and not (x <= Car.x   and y >= Car.y + Car.height):
                    continue
                if Angle == 0 and not (x < Car.x):
                    continue
                if Angle == 90 and not (y < Car.y):
                    continue
                if Angle == 180 and not (x > Car.x + Car.width):
                    continue
                if Angle == 270 and not (y > Car.y + Car.height):
                    continue

                # Top Line
                NextDistance = DistanceForHorizontalLinesVectorSystem(x,y,Car.y,Car.x,Car.x + Car.width)
                if not NextDistance==None:
                    Distances.append(NextDistance)
                # Bottom Line
                NextDistance = DistanceForHorizontalLinesVectorSystem(x,y,Car.y + Car.height,Car.x,Car.x + Car.width)
                if not NextDistance==None:
                    Distances.append(NextDistance)
                # Left Line
                NextDistance = DistanceForVerticalLinesVectorSystem(x,y,Car.x,Car.y,Car.y + Car.height)
                if not NextDistance==None:
                    Distances.append(NextDistance)
                # Right Line
                NextDistance = DistanceForVerticalLinesVectorSystem(x,y,Car.x + Car.width,Car.y,Car.y + Car.height)
                if not NextDistance==None:
                    Distances.append(NextDistance)

            # Extract the minimum distance
            minDistance = min(Distances)
           
            # calculate the position of the intercept
            delta_X = minDistance * math.cos(math.pi * Angle / 180)
            delta_Y = minDistance * math.sin(math.pi * Angle / 180)

            # draw the distance line 
            pygame.draw.line(window,red,(x , y + Level_Offset_Y),(x + delta_X , y + delta_Y + Level_Offset_Y),3)
            
            return minDistance
            
    def findNearestCar(self):
        
        # Distances to every Car
        DistanceToCar = []

        # Position of player center
        x = self.x + self.Width/2
        y = self.y + self.Height/2
        
        for Car in Car_List:
            
            # do not check distances, if Cars are not visible in the window
            if Car.y + Car.height + Level_Offset_Y < 0:
                continue
            if Car.y + Level_Offset_Y > Window_Height:
                break
            
            # Position of Car corners
            CornerPointsCar = [(Car.x,Car.y),(Car.x+Car.width,Car.y),(Car.x,Car.y+Car.height),(Car.x+Car.width,Car.y+Car.height)]

            DistanceToCarCorners = [] 

            for CarCorner in CornerPointsCar:
                X_Diff = x - CarCorner[0]
                Y_Diff = y - CarCorner[1]

                DistanceToCarCorners.append(math.sqrt( X_Diff*X_Diff + Y_Diff*Y_Diff ))

            # only add the lowest distance to the car corner of current Car 
            DistanceToCar.append(min(DistanceToCarCorners))

        # extract the Car with the lowest distance
        minDistance = min(DistanceToCar)
        nearestCarID = DistanceToCar.index(minDistance)
        Nearest_Car = Car_List[nearestCarID]

        # draw a line from the player to the top left corner of the closest Car
        pygame.draw.line(window,black,(self.x,self.y+Level_Offset_Y),(Car.x,Car.y+Level_Offset_Y))

        return Nearest_Car


    def giveNNInput(self):

        Distances = []

        # Calculate distances to obstacle in different Angles
        for Angle in range(0,181,30):
            Distances.append(self.getDistanceForAngle(Angle))
        
        # Player position is also relevant for finding a decision
        PlayerData = [self.x , Window_Width - self.x , self.y + Level_Offset_Y] 
        
        
        InputData = Distances + PlayerData
        return InputData


class Car:

    height = row_height - line_width
    width = 2*row_width

    
    direction = 1 # 1 for right, -1 for left

    def __init__(self,FieldPosX,FieldPosY):
        self.x , self.y = calc_Pos_From_Field_Pos(FieldPosX,FieldPosY)
        Car_List.append(self)
        self.speed = 1

    def deleteAllCars():
        #Car_List.
        Car_List.clear()


    def move(self):
        # moves the car

        self.x = self.x + self.direction * self.speed

        # resetting the car if it crossed the window borders
        if self.direction ==1 and self.x > Window_Width:
            self.x = 0 - self.width
        elif self.direction ==-1  and self.x + self.width <0:
            self.x = Window_Width


    def moveAllCars():
        # moves all existing cars
        for Car_i in Car_List:
            Car_i.move()

    def draw(self):
        # draws car
        pygame.draw.rect(window,white,(self.x,self.y + Level_Offset_Y,self.width,self.height))

    def drawAllCars():
        # draws all existing cars
        for Car_i in Car_List:
            Car_i.draw()

    def deleteOldCars():

        # If cars are "out of bounce", i.e., if they are one entire screen away from the actual screen, they will be deleted
        Y_Border = calc_Pos_From_Field_Pos_Y(-Number_Of_Fields_y)

        for i in Car_List:
            if i.y + Level_Offset_Y <= Y_Border:
                Car_List.remove(i)
            else:
                break

def updateLevel():
    # If rows are "out of bounce", i.e., if they are one entire screen away from the actual screen, they will be deleted

    for i in level_Indices:
        if calc_Field_Pos_From_Pos_Y(Level_Offset_Y) + i <-2:
            del level_Indices[0]
            del level[0]
            if len(level)<20:
                generateLevel()
        else:

            break


gen = 0 # global variable to keep track of which generation is currently running

def start_Game(Round):
    global Level_Offset_Y,level,level_Indices
    
    Car.deleteAllCars()
    
    #Car_List.clear()
    Level_Offset_Y  = 0
    #-----Level------#
    level = [] # will contain "grass"- or "street"-Strings, to set the level
    level_Indices = [0] # contains all the Field_Pos_Y-indices of existing rows
                    # only existing (and visible) rows should be drawn, 
                    # instead of drawing every single row that has ever been created, thus saving runtime 


    CurrentLevel = AllLevels[Round]
    CurrentDirections = AllDirections[Round]
    CurrentOffsets = AllOffsets[Round]

    # Create level based on previously generated level data
    for i in range(len(CurrentLevel)):
        if CurrentLevel[i]=="grass":
            generateGrass(1)
        else:
            generateStreet(1,1,CurrentOffsets[i],CurrentDirections[i])

    del level_Indices[0] # remove first element of list, because 0 was only added, to avoid error 


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play CrossyRoad.
    :param config_file: location of config file
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to n_generations generations.
    n_generations = 1000
    
    # extract the best genome
    winner = p.run(eval_genomes, n_generations)

    # store the best genome
    with open('best_genome.pkl', 'wb') as f:
        pickle.dump(winner, f)



def getFastestPlayer(PlayerList):
    # returns the player from PlayerList which has the highest sxore 

    scores = []
    for player in PlayerList:
        score = player.getRealScore()
        scores.append(score)

    MaxSpeedPlayerIndex = scores.index(max(scores))
        
        
    return PlayerList[MaxSpeedPlayerIndex]



### hier weiter machen
global MaxScoreAllRounds_List,MaxScoreCurrentRound_List
MaxScoreAllRounds_List = []
MaxScoreCurrentRound_List = []

def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    players and sets their fitness based on the distance they
    reach in the game.
    """
    global window, gen,MaxScoreAllRounds_List
    gen += 1 # generation number increased by 1

    
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # player object that uses that network to play
    nets = []
    players = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(math.floor(Number_Of_Fields_x/2),2))
        ge.append(genome)

    clockTick = 300000
    clock = pygame.time.Clock()
    
    run = True


    def AllPlayersStop():
        # returns True if all players stopped running
        for player in players:
            if not player.stop:
                return False
        return True
    
    def ResetAllPlayers():
        # resets all player positions and attributes
        for player in players:
            player.stop = False
            player.reachedLevels = []
            player.time = 0
            player.score = 0
            player.speed_y = 0
            player.speed_x = 0                
            player.x = calc_Pos_From_Field_Pos_X(math.floor(Number_Of_Fields_x/2))
            player.y = calc_Pos_From_Field_Pos_Y(2)
            player.FieldPos_x = math.floor(Number_Of_Fields_x/2)
            player.FieldPos_y = 2
    
    MaxScoreAllRounds = 0
    
    for Rounds in range(NumLevels):

        MaxScoreCurrentRound = 0
        
        

        start_Game(Rounds)
        ResetAllPlayers()
        
        survived_Round = 0
        died_Round = 0

        while run and not AllPlayersStop() :

            clock.tick(clockTick)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                    break

            moveLevel(getFastestPlayer(players)) # the level should move according to the fastest player, in order to eliminate slow players

            HighestScore = 0
            FirstArgument = 0
            SecondArgument=0
            Fitness = 0

            

            Car.moveAllCars()
            draw_everything()
            

            for x, player in enumerate(players):  
                
                

                if player.stop:
                    continue

                score = (player.getRealScore())/500

                # rewarding players that crossed a level threshold
                for i in RewardLevels:
                    AlreadyCrossed =  False
                    if calc_Field_Pos_From_Pos_Y(player.y)>i: # If player position exceeds level threshold

                        for j in player.reachedLevels: # check if player was already rewarded for crossing that threshold
                            
                            if j==i:
                                AlreadyCrossed = True
                                break


                        if not AlreadyCrossed: # Do not reward a player that has already crossed that threshold
                            player.crossedLevelThreshold += 1
                            
                            # higher rewards for players that cross multiple thresholds
                            # higher rewards for players that cross thresholds faster
                            ge[x].fitness += 1/player.time* player.crossedLevelThreshold 

                            player.reachedLevels.append(i) # Store the information that player crossed this threshold
                            
                    else:
                        break

                # rewarding players that finished a level
                if calc_Field_Pos_From_Pos_Y(player.y) >= LevelLength:
                    player.stop = True
                    player.speed_y = 0
                    player.speed_x = 0  
                    player.survivedTimes += 1
                    ge[x].fitness += 1/player.time * player.survivedTimes
                    

                    survived_Round += 1

                # rewarding players that stay closer to the middle (x-axis only)
                DistanceToMiddle = abs(Window_Width/2 - player.x)
                ge[x].fitness += 1/DistanceToMiddle/1000
                
                player.time = player.time + 1 # increase player "alive"-time 
                
                score = player.getScore()
                
                if MaxScoreCurrentRound < score:
                    MaxScoreCurrentRound = score


                if score>HighestScore:
                    # set variables FirstArgument, SecondArgument and Fitness depending on stats of fastest player
                    HighestScore = score
                    FirstArgument = score
                    SecondArgument = player.getScore()
                    Fitness = ge[x].fitness
                

                if not player.is_moving():
                    # player can not make a decision if he is already moving

                    input = player.giveNNInput() # get input data for neural network
                    output = nets[x].activate(input) # get player decision based on input
                    HighestOuputIndex = output.index(max(output))

                    player.KeyPressedUp = False 
                    player.KeyPressedDown = False
                    player.KeyPressedRight = False
                    player.KeyPressedLeft = False
                    
                    # set player decision based on neural network output
                    if not HighestOuputIndex == 4: # meaning if player decided to not move

                        if HighestOuputIndex==0:
                            player.KeyPressedUp = True
                        if HighestOuputIndex==1:
                            player.KeyPressedDown = True
                        if HighestOuputIndex==2:
                            player.KeyPressedLeft = True
                        if HighestOuputIndex==3:
                            player.KeyPressedRight = True

                player.React_To_Keypressed()
                
                player.draw() 
                player.move()  

                if player.check_for_collision():
                    # player should stop if he collided with objects 
                    player.stop = True
                    died_Round += 1
                    continue


            # draw stats of player with highest score
            drawStats(FirstArgument,SecondArgument,Fitness)
   
            WindowFlip()
        
        print(f"MaxScoreCurrentRound : {MaxScoreCurrentRound}")
        MaxScoreCurrentRound_List.append(MaxScoreCurrentRound)
        if MaxScoreAllRounds < MaxScoreCurrentRound:
            MaxScoreAllRounds = MaxScoreCurrentRound

    if gen % 20 == 0:
        print(f"MaxScoreAllRounds : {MaxScoreAllRounds}")
    MaxScoreAllRounds_List.append(MaxScoreAllRounds)

    if gen % 20 == 0:
        print(f"MaxScoreAllRounds_List : {MaxScoreAllRounds_List}")
        print(f"MaxScoreCurrentRound_List : {MaxScoreCurrentRound_List}")


    def Count_Times_Of_Player_Survival():
        # prints how many players survived 0, 1, 2 ... n times
        for i in range(NumLevels+1):
            numPlayers = FindPlayersThatSurvivedXTimes(i)
            print(f"{numPlayers} Players survived {i} Rounds")

    def FindPlayersThatSurvivedXTimes(x):
        # returns the number of players that survived x rounds
        numPlayers = 0
        for player in players:
            if player.survivedTimes == x:
                numPlayers +=1
        return numPlayers
    
    Count_Times_Of_Player_Survival()
    

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NEAT_Configuration.txt')
    run(config_path)





