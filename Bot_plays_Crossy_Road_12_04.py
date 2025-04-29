import pygame

import random
import math



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
Level_Offset_Y = 0
Level_Speed = -1


#-----Window------#
window = pygame.display.set_mode((Window_Width,Window_Height))
pygame.display.set_caption('DZT_Spiel')




def generateLevel():
    # generates all layers for the level --> Grass- and Street-Layers

    generateGrass()
    generateStreet() 

    if len(level)<2*Number_Of_Fields_y: # add further levels if levels are running out
        generateLevel()

def generateGrass(Number_Of_Rows=random.choice([ 2, 3])):
    # generates a random number of grass layers and adds them to the level 

    for i in range(Number_Of_Rows):
        level.append("grass")
        level_Indices.append(level_Indices[-1] + 1) # add next indice with indice-number increased by one 

def generateStreet():
    # generates one street layer and adds it to the level 
    
    
    Number_Of_Rows = 1

    for i in range(Number_Of_Rows):
        level.append("street")
        level_Indices.append(level_Indices[-1] + 1) # add next indice with indice-number increased by one 

    SpaceBetweenCars = 2.9 # fields
    CarSpeed = 1 # pixels per frame

    NumCars = math.ceil(Number_Of_Fields_x/(2 + SpaceBetweenCars))  # Number of cars for next street


    Field_Pos_Y = level_Indices[-1] - Number_Of_Rows + 1 # get Field position of next street


    # Iterate through every Street that should be appended
    # (Number of Streets can currently only be one)
    for i in range(Number_Of_Rows):
        
        Field_Pos_X = 1
        x_disposition = random.choice([0, 0.4, 0.8, 1.2, 1.6, 2]) # get a random x-disposition so not all cars are running parallel to each other
        direction = random.choice([1, -1])  # random Car direction : left or right


        # Iterate through every Car that should be added
        for j in range(NumCars):
            
            currentCar = Car(Field_Pos_X + x_disposition,Field_Pos_Y)   # add next Car
            currentCar.direction = direction    # set direction
            currentCar.speed = CarSpeed         # set speed

            Field_Pos_X = Field_Pos_X + 2 + SpaceBetweenCars    # Increase Field_Pos_X for next Car in current Row
        
        Field_Pos_Y = Field_Pos_Y + 1   # Increase Field_Pos_Y for next Row

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


        self.score = 0
        self.time = 0
        self.stop = False # set to true when player collides with car or level window borders
        self.LastDecision = ""  # direction of last move 
    
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
            



class Car:

    height = row_height - line_width
    width = 2*row_width

    
    direction = 1 # 1 for right, -1 for left

    def __init__(self,FieldPosX,FieldPosY):
        self.x , self.y = calc_Pos_From_Field_Pos(FieldPosX,FieldPosY)
        Car_List.append(self)
        self.speed = 1


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
    global level,level_Indices,Level_Offset_Y
    Y_Border = calc_Pos_From_Field_Pos_Y(-Number_Of_Fields_y)

    for i in level_Indices:
        if calc_Field_Pos_From_Pos_Y(Level_Offset_Y) + i <-2:
            del level_Indices[0]
            del level[0]
            if len(level)<2*Number_Of_Fields_y:
                generateLevel()
        else:

            break

def create_Start_Levels():
    # creates a the level
    global Level_Offset_Y,level,level_Indices
    

    generateGrass(3)
    generateStreet()
    generateLevel()

    del level_Indices[0] # remove first element of list, because 0 was only added, to avoid error 

    




def determine_best_move(Bot):

    global Level_Offset_Y

    # Store Level and Car positions before simulating outcomes 
    # for diferent decisions, so that each time the original 
    # positions can be restored
    CarPosX_Before = []
    CarPosY_Before = []
    Level_Offset_Y_Before = Level_Offset_Y

    for CarX in Car_List:
        CarPosX_Before.append(CarX.x)
        CarPosY_Before.append(CarX.y)


    def ReturnCarsToOriginalPos():
        # returns Cars to their original positions before decision simulation
        for CarID,CarX in enumerate(Car_List):
            CarX.x = CarPosX_Before[CarID]
            CarX.y = CarPosY_Before[CarID]

                    
    FieldPosX = calc_Field_Pos_From_Pos_X(Bot.x)
    FieldPosY = calc_Field_Pos_From_Pos_Y(Bot.y)

    # Clone Bot and simulate Down-Keypress
    PlayerDown = Player(FieldPosX,FieldPosY)
    PlayerDown.KeyPressedDown = True
    PlayerDown.React_To_Keypressed()

    # Clone Bot and simulate Left-Keypress  
    PlayerLeft = Player(FieldPosX,FieldPosY)
    PlayerLeft.KeyPressedLeft = True
    PlayerLeft.React_To_Keypressed()

    # Clone Bot and simulate Right-Keypress
    PlayerRight = Player(FieldPosX,FieldPosY)
    PlayerRight.KeyPressedRight = True
    PlayerRight.React_To_Keypressed()

    # Moving down should be preferred
    # Only consider moving left or right if 
    # obstacles are in the way 
    MoveDown = True
    MoveRight = False
    MoveLeft = False
    

    # simulate Down-movement of player until the next Field is reached
    # set MoveDown to False if player hits obstacle along the way
    while PlayerDown.is_moving():
        PlayerDown.move()
        if PlayerDown.check_for_collision():
            MoveDown = False
        Car.moveAllCars()
        moveLevel(Bot)

    # Restore original Level and Car positions after simulation
    ReturnCarsToOriginalPos()
    Level_Offset_Y = Level_Offset_Y_Before

    

    if not MoveDown:
        # simulate right- and left-movement of player if 
        # down-movement is not possible
         
        MoveRight = True
    
        
        # simulate Right-movement of player until the next Field is reached
        # set MoveRight to False if player hits obstacle along the way
        while PlayerRight.is_moving():
            PlayerRight.move()
            if PlayerRight.check_for_collision():
                MoveRight = False
            Car.moveAllCars()
            moveLevel(Bot)

        # Restore original Level and Car positions after simulation
        ReturnCarsToOriginalPos()
        Level_Offset_Y = Level_Offset_Y_Before

    
    
        MoveLeft = True

        # simulate Left-movement of player until the next Field is reached
        # set MoveLeft to False if player hits obstacle along the way
        while PlayerLeft.is_moving():
            PlayerLeft.move()
            if PlayerLeft.check_for_collision():
                MoveLeft = False
            Car.moveAllCars()
            moveLevel(Bot)

        # Restore original Level and Car positions after simulation
        ReturnCarsToOriginalPos()
        Level_Offset_Y = Level_Offset_Y_Before


    if MoveRight and MoveLeft:
        # If both right- and left-movement is possible 
        # moving right is preferred if player is on the left half of the screen
        # unless the last decision was to move left. 
        # This is in order to avoid the player continuously moving left and right 
        # in a cylcle until the obstacle is gone  

        # moving left is preferred if player is on the right half of the screen
        # unless the last decision was to move right. 
        # This is in order to avoid the player continuously moving left and right 
        # in a cylcle until the obstacle is gone  


        if Bot.x + Bot.Width/2 <= Window_Width/2:
            if Bot.LastDecision == "MoveLeft":
                MoveRight = False
            else:
                MoveLeft = False
            
            
        else:
            if Bot.LastDecision == "MoveRight":
                MoveLeft = False
            else:
                MoveRight = False

    # FInallize the decision and save it in LastDecision
    if MoveDown:
        Bot.KeyPressedDown = True
        Bot.LastDecision = "MoveDown"
    elif MoveRight:
        Bot.KeyPressedRight = True
        Bot.LastDecision = "MoveRight"
    elif MoveLeft:
        Bot.KeyPressedLeft = True
        Bot.LastDecision = "MoveLeft"
    else:
        Bot.LastDecision = ""

    # del PlayerDown,PlayerRight,PlayerLeft
    
    # delete references to simulated players
    PlayerDown = None
    PlayerRight = None
    PlayerLeft = None

    

def Start_Bot_Game():
    # starts the game
    
    create_Start_Levels()
    
    clockTick = 30000 # Frames per second
    clock = pygame.time.Clock()
    run = True
    
    Bot = Player(math.floor(Number_Of_Fields_x/2),2) # create Bot

    


    while run: # game loop
            

        clock.tick(clockTick)


        for event in pygame.event.get(): # stop programm if window was closed
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break


        global Level_Offset_Y, level,level_Indices
        
        updateLevel() 
        draw_everything()


        if not Bot.is_moving():
            
            determine_best_move(Bot) 

        Bot.React_To_Keypressed()
        
        Bot.move()

        if Bot.check_for_collision():

            Bot.stop = True
            print("Bot died")
            print(Bot.score)
            run = False
            continue

        Bot.draw()
        Bot.score = Bot.getScore()
        Bot.drawScore()

        moveLevel(Bot)
        Car.moveAllCars()

        WindowFlip()
        Car.deleteOldCars()





Start_Bot_Game()


