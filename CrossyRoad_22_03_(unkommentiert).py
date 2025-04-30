import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# -----Colors------#
# Define RGB color codes for different colors used in the game
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)

# -----Lines------#
# Define grid line width and dimensions of rows/columns in the grid
line_width = 4
row_height = 50 + line_width
row_width = 50 + line_width

# -----Window------#
# Set the number of fields (rows and columns) and calculate window size
Number_Of_Fields_x = 20  # Number of fields horizontally
Number_Of_Fields_y = 12  # Number of fields vertically
Window_Width = row_height * Number_Of_Fields_x + line_width
Window_Height = row_width * Number_Of_Fields_y + line_width
Level_Offset_Y = 0  # Vertical offset for scrolling
Level_Speed = -1  # Speed at which the level scrolls upwards

# Initialize the game window
window = pygame.display.set_mode((Window_Width, Window_Height))
pygame.display.set_caption('DZT_Spiel')  # Set the game window title

# Define font for rendering text (used for displaying scores, etc.)
font = pygame.font.Font(None, 80)

# -----Level------#
# Lists to manage level rows and their indices
level = []  # Contains strings like "grass" or "street" to indicate row types
level_Indices = [0]  # Stores vertical indices of each row in the level


def generateLevel():
    """
    Recursively generates the game level by adding grass and street rows.
    Ensures that at least three screens worth of rows are generated.
    """
    generateGrass()  # Add grass rows
    generateStreet()  # Add street rows
    if len(level) < 3 * Number_Of_Fields_y:  # Ensure sufficient rows
        generateLevel()


def generateGrass():
    """
    Adds a random number of grass rows to the level.
    """
    Number_Of_Rows = random.choice([1, 2, 3])  # Randomly choose 1-3 rows
    for i in range(Number_Of_Rows):
        level.append("grass")  # Append "grass" to the level
        level_Indices.append(level_Indices[-1] + 1)  # Update indices


def generateStreet():
    """
    Adds a random number of street rows to the level.
    Configures cars for each street row based on difficulty settings.
    """
    Number_Of_Rows = random.choice([1, 2, 3])  # Randomly choose 1-3 rows
    for i in range(Number_Of_Rows):
        level.append("street")  # Append "street" to the level
        level_Indices.append(level_Indices[-1] + 1)  # Update indices by incrementing the last index by 1

    # Set difficulty parameters for the street
    RoadDifficulty = random.choice([1, 2, 3])  # Randomly choose difficulty
    if RoadDifficulty == 1:
        SpaceBetweenCars = 5  # Larger gaps between cars
        CarSpeed = 2  # Faster cars
    elif RoadDifficulty == 2:
        SpaceBetweenCars = 4
        CarSpeed = 1.5
    elif RoadDifficulty == 3:
        SpaceBetweenCars = 3.5  # Smaller gaps between cars
        CarSpeed = 1  # Slower cars

    NumCars = math.ceil(Number_Of_Fields_x / (2 + SpaceBetweenCars))  # Calculate the number of cars

    Field_Pos_Y = level_Indices[-1] - Number_Of_Rows + 1  # Get starting position for the street rows
    for i in range(Number_Of_Rows):
        direction = random.choice([1, -1])  # Random direction (right or left)
        Field_Pos_X = 1
        x_disposition = random.choice([0, 0.4, 0.8, 1.2, 1.6, 2])  # Random initial offset

        for j in range(NumCars):
            currentCar = Car(Field_Pos_X + x_disposition, Field_Pos_Y)  # Create a car
            currentCar.direction = direction  # Set car direction
            currentCar.speed = CarSpeed  # Set car speed
            Field_Pos_X = Field_Pos_X + 2 + SpaceBetweenCars  # Update position for the next car
        Field_Pos_Y = Field_Pos_Y + 1  # Move to the next row


def moveLevel():
    """
    Scrolls the level upwards as the player progresses.
    Adjusts speed based on player movement.
    """
    global Level_Offset_Y  # Access the global vertical offset

    if Level_Speed < -player1.speed_y * row_height or player1.y + Level_Offset_Y < 5 * row_height:
        # Normal scrolling speed
        Level_Offset_Y = Level_Offset_Y + Level_Speed
    else:
        # Faster scrolling if the player is moving quickly
        Level_Offset_Y = Level_Offset_Y - player1.speed_y * row_height


def draw_number(number, x, y):
    """
    Renders a number at the specified position on the screen.
    """
    text = font.render(str(number), True, black)  # Render the number as text
    window.blit(text, (x, y))  # Display the text on the screen


def draw_level():
    """
    Draws the rows of the level onto the game window.
    Grass rows are green, and street rows are black.
    """
    for i in range(len(level)):  # Iterate through all rows
        if level[i] == "grass":
            currentColor = green
        else:
            currentColor = black

        # Draw the row as a rectangle
        pygame.draw.rect(window, currentColor,
                         (0, Level_Offset_Y + (level_Indices[i] - 1) * row_height, Window_Width, row_height))


def calc_Field_Pos_From_Pos(Pos_x, Pos_y):
    """
    Converts screen coordinates into field grid coordinates.
    """
    Field_pos_x = (Pos_x - line_width) / row_width + 1
    Field_pos_y = (Pos_y - line_width) / row_height + 1
    return Field_pos_x, Field_pos_y


def calc_Field_Pos_From_Pos_X(Pos_x):
    """
    Converts the X coordinate from screen to field grid.
    """
    Field_pos_x, _ = calc_Field_Pos_From_Pos(Pos_x, 0)
    return Field_pos_x


def calc_Field_Pos_From_Pos_Y(Pos_y):
    """
    Converts the Y coordinate from screen to field grid.
    """
    _, Field_pos_y = calc_Field_Pos_From_Pos(0, Pos_y)
    return Field_pos_y


def calc_Pos_From_Field_Pos(Field_pos_x, Field_pos_y):
    """
    Converts field grid coordinates to screen coordinates.
    """
    Pos_x = line_width + (Field_pos_x - 1) * row_width
    Pos_y = line_width + (Field_pos_y - 1) * row_height
    return Pos_x, Pos_y

def calc_Pos_From_Field_Pos_X(Field_pos_x):
    """
    Converts the X coordinate from field grid to screen.
    """
    Pos_x, _ = calc_Pos_From_Field_Pos(Field_pos_x, 0)
    return Pos_x

def calc_Pos_From_Field_Pos_Y(Field_pos_y):
    """
    Converts the X coordinate from field grid to screen.
    """
    _, Pos_y = calc_Pos_From_Field_Pos(0, Field_pos_y)
    return Pos_y

def drawGrid():
    """
    Draws the grid lines for the game field.
    """
    for i in range(Number_Of_Fields_x + 1):
        # Vertical grid lines
        pygame.draw.rect(window, blue, ((i) * row_width, 0, line_width, Window_Height))

    for i in range(len(level_Indices)):
        # Horizontal grid lines
        pygame.draw.rect(window, blue, (0, (level_Indices[i] - 1) * row_height + Level_Offset_Y, Window_Width, line_width))


def draw_everything():
    """
    Draws all game elements including the level, grid, cars, and player.
    """
    window.fill(white)  # Clear the screen
    draw_level()  # Draw the level rows
    drawGrid()  # Draw the grid lines
    Car.drawAllCars()  # Draw all cars
    player1.draw()  # Draw the player
    player1.drawScore()  # Draw the player's score
    pygame.display.flip()  # Update the display

class Player:
    """
    Represents the player character in the game.
    Handles movement, drawing, and scoring logic.
    """
    # Dimensions of the player
    Width = row_width - line_width
    Height = row_height - line_width
    # Initial speed and scoring parameters
    speed_x = 0
    speed_y = 0
    Normal_Player_Speed = 1 / 10  # Speed in blocks per frame; must be between 0 and 1
    score = 0

    def __init__(self, FieldPos_x, FieldPos_y):
        """
        Initializes the player with a starting position in the grid.
        """
        self.FieldPos_x = FieldPos_x
        self.FieldPos_y = FieldPos_y
        self.x, self.y = calc_Pos_From_Field_Pos(FieldPos_x, FieldPos_y)

    def move(self):
        """
        Updates the player's position based on their current speed.
        """
        self.updatePlayerSpeed()
        self.x = self.x + self.speed_x * row_height
        self.y = self.y + self.speed_y * row_height

    def draw(self):
        """
        Draws the player character as a red rectangle on the screen.
        """
        pygame.draw.rect(window, red, (self.x, self.y + Level_Offset_Y, self.Width, self.Height))

    def is_moving(self):
        """
        Checks if the player is currently moving.
        Returns True if the player has non-zero speed.
        """
        return self.speed_x != 0 or self.speed_y != 0

    def React_To_Keypressed(self, keys):
        """
        Reacts to keyboard input to update the player's speed.
        Only processes input if the player is not already moving.
        """
        if not self.is_moving():
            if keys[pygame.K_DOWN]:
                self.speed_y = self.Normal_Player_Speed
            elif keys[pygame.K_UP]:
                self.speed_y = -self.Normal_Player_Speed
            elif keys[pygame.K_RIGHT]:
                self.speed_x = self.Normal_Player_Speed
            elif keys[pygame.K_LEFT]:
                self.speed_x = -self.Normal_Player_Speed

    def updatePlayerSpeed(self):
        """
        Stops the player when they reach a new field.
        Updates the player's field position and ensures they stay aligned with the grid.
        """
        # Moving down
        if self.speed_y > 0:
            if self.y + self.speed_y * row_height > calc_Pos_From_Field_Pos_Y(self.FieldPos_y + 1):
                self.speed_y = 0
                self.FieldPos_y += 1
                self.x, self.y = calc_Pos_From_Field_Pos(self.FieldPos_x, self.FieldPos_y)
        # Moving up
        elif self.speed_y < 0:
            if self.y + self.speed_y * row_height < calc_Pos_From_Field_Pos_Y(self.FieldPos_y - 1):
                self.speed_y = 0
                self.FieldPos_y -= 1
                self.x, self.y = calc_Pos_From_Field_Pos(self.FieldPos_x, self.FieldPos_y)

        # Moving right
        if self.speed_x > 0:
            if self.x + self.speed_x * row_width > calc_Pos_From_Field_Pos_X(self.FieldPos_x + 1):
                self.speed_x = 0
                self.FieldPos_x += 1
                self.x, self.y = calc_Pos_From_Field_Pos(self.FieldPos_x, self.FieldPos_y)
        # Moving left
        elif self.speed_x < 0:
            if self.x + self.speed_x * row_width < calc_Pos_From_Field_Pos_X(self.FieldPos_x - 1):
                self.speed_x = 0
                self.FieldPos_x -= 1
                self.x, self.y = calc_Pos_From_Field_Pos(self.FieldPos_x, self.FieldPos_y)

    def getScore(self):
        """
        Calculates the player's score based on their highest position reached.
        Updates the score if the player moves to a higher field.
        """
        currentScore = calc_Field_Pos_From_Pos_Y(self.y)
        if self.score < currentScore:
            self.score = currentScore

    def drawScore(self):
        """
        Draws the player's score in the bottom-left corner of the screen.
        """
        rounded_score = math.floor(self.score)
        num_digits = len(str(rounded_score))
        # Clear the previous score display
        pygame.draw.rect(window, white, (0, Window_Height - row_height, num_digits * row_width, row_height))
        # Draw the new score
        draw_number(rounded_score, 10, Window_Height - row_height)


class Car:
    """
    Represents a car object that moves on street rows.
    Handles movement, drawing, and deletion of old cars.
    """
    global Car_List
    Car_List = []  # List to store all car objects
    # Dimensions of the car
    height = row_height - line_width
    width = 2 * row_width

    direction = 1  # Direction of the car (1 for right, -1 for left)

    def __init__(self, FieldPosX, FieldPosY):
        """
        Initializes a car at the specified position in the grid.
        """
        self.x, self.y = calc_Pos_From_Field_Pos(FieldPosX, FieldPosY)
        Car_List.append(self)  # Add the car to the global car list
        self.speed = 1

    def move(self):
        """
        Updates the car's position based on its speed and direction.
        Wraps the car around to the opposite side if it moves out of bounds.
        """
        self.x = self.x + self.direction * self.speed
        if self.direction == 1 and self.x > Window_Width:
            self.x = 0 - self.width
        elif self.direction == -1 and self.x + self.width < 0:
            self.x = Window_Width

    @staticmethod
    def moveAllCars():
        """
        Moves all cars in the global car list.
        """
        for Car_i in Car_List:
            Car_i.move()

    def draw(self):
        """
        Draws the car as a white rectangle on the screen.
        """
        pygame.draw.rect(window, white, (self.x, self.y + Level_Offset_Y, self.width, self.height))

    @staticmethod
    def drawAllCars():
        """
        Draws all cars in the global car list.
        """
        for Car_i in Car_List:
            Car_i.draw()

    @staticmethod
    def deleteOldCars():
        """
        Deletes cars that are far outside the visible area of the screen.
        """
        Y_Border = calc_Pos_From_Field_Pos_Y(-Number_Of_Fields_y)
        for i in Car_List:
            if i.y + Level_Offset_Y <= Y_Border:
                Car_List.remove(i)
            else:
                break


def updateLevel():
    """
    Updates the level by removing rows that are far outside the visible area.
    Generates new rows if necessary to maintain a consistent level length.
    """
    Y_Border = calc_Pos_From_Field_Pos_Y(-Number_Of_Fields_y)
    for i in level_Indices:
        if calc_Field_Pos_From_Pos_Y(Level_Offset_Y) + i < -2:
            del level_Indices[0]
            del level[0]
            if len(level) < 20:
                generateLevel()
                print("new Level generated")
        else:
            break


def check_for_collision():
    """
    Checks if the player has collided with any cars or gone out of bounds.
    """
    # Check if the player is out of bounds
    if (player1.x < 0 or player1.y + Level_Offset_Y < 0 or
            player1.x + player1.Width >= Window_Width or
            player1.y + player1.Height + Level_Offset_Y >= Window_Height):
        return True

    # Check for collisions with cars
    Player_Field_Pos_Y = calc_Field_Pos_From_Pos_Y(player1.y)
    for i in Car_List:
        Car_Field_Pos_Y = calc_Field_Pos_From_Pos_Y(i.y)
        if Player_Field_Pos_Y + 2 < Car_Field_Pos_Y:
            continue
        # Check collision with each corner of the player
        if (player1.x >= i.x and player1.x <= i.x + i.width and
                player1.y >= i.y and player1.y <= i.y + i.height):
            return True
        if (player1.x + player1.Width >= i.x and player1.x + player1.Width <= i.x + i.width and
                player1.y >= i.y and player1.y <= i.y + i.height):
            return True
        if (player1.x >= i.x and player1.x <= i.x + i.width and
                player1.y + player1.Height >= i.y and player1.y + player1.Height <= i.y + i.height):
            return True
        if (player1.x + player1.Width >= i.x and player1.x + player1.Width <= i.x + i.width and
                player1.y + player1.Height >= i.y and player1.y + player1.Height <= i.y + i.height):
            return True
    return False


def start_Game():
    """
    Initializes the game by generating the initial level and creating the player.
    """
    generateGrass()
    generateGrass()
    generateLevel()
    del level_Indices[0]  # Remove the first element to avoid errors
    global player1
    player1 = Player(2, 3)


# Start the game
start_Game()

# Main game loop
run = True
clock = pygame.time.Clock()

while run:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            player1.React_To_Keypressed(pygame.key.get_pressed())

    # Game logic
    player1.move()
    Car.moveAllCars()
    Car.deleteOldCars()
    player1.getScore()
    updateLevel()
    draw_everything()
    moveLevel()  # Update the level's vertical position


    # Check for collisions
    if check_for_collision():
        run = False

    clock.tick(60)  # Limit to 60 FPS

# Quit Pygame
pygame.quit()
