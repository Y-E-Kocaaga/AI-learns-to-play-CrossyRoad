import pygame
import sys
import random
import math

pygame.init()



#-----Colors------#
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0,0,255)
green = (0,255,0)
black = (0,0,0)


#-----Lines------#
line_width = 4
row_height = 50 + line_width
row_width = 50 + line_width

#-----Window------#
Number_Of_Fields_x = 20
Number_Of_Fields_y = 12
Window_Width = row_height * Number_Of_Fields_x + line_width
Window_Height = row_width * Number_Of_Fields_y + line_width
Level_Offset_Y = 0
Level_Speed = -1

#-----Window------#
window = pygame.display.set_mode((Window_Width,Window_Height))
pygame.display.set_caption('DZT_Spiel')

font = pygame.font.Font(None, 80)


#-----Level------#
level = [] # will contain "grass"- or "street"-Strings, to set the level
level_Indices = [0] # contains all the Field_Pos_Y-indices of existing rows
                    # only existing (and visible) rows should be drawn, 
                    # instead of drawing every single row that has ever been created, thus saving runtime 








def generateLevel():
    
    generateGrass()
    generateStreet() 
    print(level)
    if len(level)<3*Number_Of_Fields_y:
        generateLevel()

def generateGrass():
    Number_Of_Rows = random.choice([1, 2, 3])

    print(Number_Of_Rows)
    for i in range(Number_Of_Rows):
        level.append("grass")
        level_Indices.append(level_Indices[-1] + 1) # add next indice with indice-number increased by one 

def generateStreet():
    Number_Of_Rows = random.choice([1, 2, 3])
    #Number_Of_Rows = 2
    print(Number_Of_Rows)
    for i in range(Number_Of_Rows):
        level.append("street")
        level_Indices.append(level_Indices[-1] + 1) # add next indice with indice-number increased by one 

    RoadDifficulty = random.choice([1, 2, 3])
    #RoadDifficulty = 1
    if RoadDifficulty == 1:
        SpaceBetweenCars = 5
        CarSpeed = 2
    elif RoadDifficulty == 2:
        SpaceBetweenCars = 4
        CarSpeed = 1.5
    elif RoadDifficulty == 3:
        SpaceBetweenCars = 3.5
        CarSpeed = 1

    NumCars = math.ceil(Number_Of_Fields_x/(2 + SpaceBetweenCars))
    print("NumCars")
    print(NumCars)

    #Field_Pos_Y = len(level) - Number_Of_Rows + 1
    Field_Pos_Y = level_Indices[-1] - Number_Of_Rows + 1
    for i in range(Number_Of_Rows):
        direction = random.choice([1, -1])
        Field_Pos_X = 1
        x_disposition = random.choice([0, 0.4, 0.8, 1.2, 1.6, 2])
        
        for j in range(NumCars):
            
            currentCar = Car(Field_Pos_X + x_disposition,Field_Pos_Y)
            currentCar.direction = direction
            currentCar.speed = CarSpeed
            Field_Pos_X = Field_Pos_X + 2 + SpaceBetweenCars
        Field_Pos_Y = Field_Pos_Y + 1

def moveLevel():
    global Level_Offset_Y

    
    if Level_Speed<-player1.speed_y*row_height or player1.y + Level_Offset_Y < 5*row_height:
        
        Level_Offset_Y = Level_Offset_Y + Level_Speed
    else:
        
        Level_Offset_Y = Level_Offset_Y - player1.speed_y*row_height

def draw_number(number, x, y):
    text = font.render(str(number), True, black)
    window.blit(text, (x, y))

def draw_level():

    for i in range(len(level)):

        if level[i] == "grass":
            currentColor = green
        else:
            currentColor = black
        

        pygame.draw.rect(window,currentColor,(0,Level_Offset_Y + (level_Indices[i] - 1) * row_height,Window_Width,row_height))
    



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

def  get_player_Field_pos_x(player):
    (Field_pos_x,Field_pos_y) = get_player_Field_pos(player)
    return Field_pos_x


def  get_player_Field_pos_y(player):
    (Field_pos_x,Field_pos_y) = get_player_Field_pos(player)
    return Field_pos_y



def drawGrid():
    for i in range(Number_Of_Fields_x+1):
        pygame.draw.rect(window, blue,((i) * row_width,0,line_width,Window_Height))
 
    for i in range(len(level_Indices)):
        pygame.draw.rect(window, blue,(0,(level_Indices[i] - 1)* row_height + Level_Offset_Y,Window_Width,line_width))

    




def draw_everything():

    window.fill(white)

    
    draw_level()
    drawGrid()
    Car.drawAllCars()

    player1.draw()
    moveLevel()
    player1.drawScore()

    pygame.display.flip()



class Player:
    
    Width = row_width -  line_width
    Height = row_height - line_width
    speed_x = 0
    speed_y = 0
    Normal_Player_Speed = 1/10 # Blocks per Frame; muss zwischen 0 und 1 liegen
    score = 0

    def __init__(self, FieldPos_x, FieldPos_y):
        self.FieldPos_x = FieldPos_x
        self.FieldPos_y = FieldPos_y
        self.x , self.y = calc_Pos_From_Field_Pos(FieldPos_x,FieldPos_y)
    
    def move(self):
        self.updatePlayerSpeed()
        self.x = self.x + self.speed_x * row_height
        self.y = self.y + self.speed_y * row_height

    def draw(self):
        pygame.draw.rect(window, red, (self.x,self.y + Level_Offset_Y,self.Width,self.Height))

    def is_moving(self):
        return self.speed_x != 0 or self.speed_y != 0 

    def React_To_Keypressed(self,keys):
        if self.is_moving() == False:
                if keys[pygame.K_DOWN]:
                    self.speed_y = self.Normal_Player_Speed
                elif keys[pygame.K_UP]:
                    self.speed_y = -self.Normal_Player_Speed 
                elif keys[pygame.K_RIGHT]:
                    self.speed_x = self.Normal_Player_Speed 
                elif keys[pygame.K_LEFT]:
                    self.speed_x = -self.Normal_Player_Speed

    def updatePlayerSpeed(self):
        if self.speed_y>0:
            if self.y + self.speed_y * row_height > calc_Pos_From_Field_Pos_Y(self.FieldPos_y+1):
                self.speed_y = 0
                self.FieldPos_y = self.FieldPos_y + 1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
        
        elif self.speed_y<0:
            if self.y + self.speed_y * row_height < calc_Pos_From_Field_Pos_Y(self.FieldPos_y-1):
                self.speed_y = 0
                self.FieldPos_y = self.FieldPos_y + -1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
        
        if self.speed_x>0:
            if self.x + self.speed_x * row_width > calc_Pos_From_Field_Pos_X(self.FieldPos_x+1):
                self.speed_x = 0
                self.FieldPos_x = self.FieldPos_x + 1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
        
        elif self.speed_x<0:
            if self.x + self.speed_x * row_width < calc_Pos_From_Field_Pos_X(self.FieldPos_x-1):
                self.speed_x = 0
                self.FieldPos_x = self.FieldPos_x + -1
                self.x , self.y = calc_Pos_From_Field_Pos(self.FieldPos_x,self.FieldPos_y)
    def getScore(self):

        

        #currentScore = player1.y - Level_Offset_Y
        currentScore = calc_Field_Pos_From_Pos_Y(self.y)
        if self.score<currentScore:
            self.score = currentScore

    def drawScore(self):
        

        rounded_score = math.floor(self.score)
        num_digits = len(str(rounded_score))
        pygame.draw.rect(window,white,(0,Window_Height-row_height,num_digits*row_width,row_height))


        draw_number(rounded_score,10,Window_Height-row_height)

class Car:
    global Car_List
    Car_List = []
    height = row_height - line_width
    width = 2*row_width

    
    direction = 1 # 1 for right, -1 for left

    def __init__(self,FieldPosX,FieldPosY):
        self.x , self.y = calc_Pos_From_Field_Pos(FieldPosX,FieldPosY)
        Car_List.append(self)
        self.speed = 1

    def move(self):
        self.x = self.x + self.direction * self.speed
        if self.direction ==1 and self.x > Window_Width:
            self.x = 0 - self.width
        elif self.direction ==-1  and self.x + self.width <0:
            self.x = Window_Width


    def moveAllCars():
        for Car_i in Car_List:
            Car_i.move()

    def draw(self):
        pygame.draw.rect(window,white,(self.x,self.y + Level_Offset_Y,self.width,self.height))

    def drawAllCars():
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
    Y_Border = calc_Pos_From_Field_Pos_Y(-Number_Of_Fields_y)

    for i in level_Indices:
        if calc_Field_Pos_From_Pos_Y(Level_Offset_Y) + i <-2:
            del level_Indices[0]
            del level[0]
            if len(level)<20:
                generateLevel()
                print("new Level generated")
        else:

            break




def check_for_collision():
    # check if player is outside of boundaries
    if player1.x<0 or player1.y + Level_Offset_Y<0 or player1.x + player1.Width >= Window_Width or player1.y + player1.Height + Level_Offset_Y >= Window_Height:
        return True
    

    # check if cars are colliding with player

    Player_Field_Pos_Y = calc_Field_Pos_From_Pos_Y(player1.y)
    for i in Car_List:
        Car_Field_Pos_Y = calc_Field_Pos_From_Pos_Y(i.y)
        if Player_Field_Pos_Y +2 < Car_Field_Pos_Y:
            continue
        #if Player_Field_Pos_Y + 2 > Car_Field_Pos_Y:
        #    break
        # check top left corner of player
        if (player1.x >= i.x and player1.x <= i.x + i.width) and (player1.y  >= i.y and player1.y <= i.y + i.height):
            return True
        # check top right corner of player
        if (player1.x + player1.Width >= i.x and player1.x + player1.Width <= i.x + i.width) and (player1.y >= i.y and player1.y <= i.y + i.height):
            return True
        # check bottom left corner of player
        if (player1.x >= i.x and player1.x <= i.x + i.width) and (player1.y  + player1.Height >= i.y and player1.y  + player1.Height <= i.y + i.height):
            return True
        # check bottom right corner of player
        if (player1.x + player1.Width >= i.x and player1.x + player1.Width <= i.x + i.width) and (player1.y + player1.Height >= i.y and player1.y + player1.Height <= i.y + i.height):
            return True


def start_Game():
    generateGrass()
    generateGrass()
    generateLevel()
    del level_Indices[0] # remove first element of list, because 0 was only added, to avoid error 
    global player1, car1, car2
    player1 = Player(2,3)


start_Game()

run = True
clock = pygame.time.Clock()


while run:
    
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN : 
            player1.React_To_Keypressed(pygame.key.get_pressed())
            
    player1.move()
    Car.moveAllCars()
    Car.deleteOldCars()
    player1.getScore()
    updateLevel()
    draw_everything()

    if check_for_collision():
        run = False

    clock.tick(60)


pygame.quit()