import pygame as pg
import os
import random as rand
pg.init()

# Global Constants
#Set Screen Dimensions
window_height = 500
window_width = 1150

# Initializing Obstacles

tiny_cactus = [pg.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pg.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pg.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
large_cactus = [pg.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pg.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pg.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

birds_images = [pg.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pg.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

clouds_images = pg.image.load(os.path.join("Assets/Other", "Cloud.png"))

#
SCREEN = pg.display.set_mode((window_width, window_height))

sprinting_animation = [pg.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pg.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
hopping_animation = pg.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
crouching_animation = [pg.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pg.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

BG = pg.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    #initializing variables
    dist_x = 80
    dist_y = 310
    duck_pos_y = 340
    vel_jmp = 8.5

    def __init__(self):
        #loading images
        self.crouch_img = crouching_animation
        self.sprinting_img = sprinting_animation
        self.hopping_img = hopping_animation
        #initial state
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        # animation variables
        self.step_index = 0
        self.jump_vel = self.vel_jmp
        self.image = self.sprinting_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.dist_x
        self.dino_rect.y = self.dist_y

    def update(self, userInput):
        #updating state of dinasaur
        if self.dino_duck:
            self.crouch()
        if self.dino_run:
            self.sprint()
        if self.dino_jump:
            self.hopp()


        if self.step_index >= 10:
            self.step_index = 0
        #checking key press
        if userInput[pg.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pg.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pg.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def crouch(self):
        #updating image for crouching animation
        self.image = self.crouch_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.dist_x
        self.dino_rect.y = self.duck_pos_y
        self.step_index += 1

    def sprint(self):
        #updating image for sprinting animation
        self.image = self.sprinting_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.dist_x
        self.dino_rect.y = self.dist_y
        self.step_index += 1

    def hopp(self):
        #updating image for hopping animation
        self.image = self.hopping_img
        if self.dino_jump:
            #considering velocity aspect
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        #cheking if hopp ends    
        if self.jump_vel < - self.vel_jmp:
            self.dino_jump = False
            self.jump_vel = self.vel_jmp

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# dispaly  clouds on the screen 
class Cloud:
    #initializes new cloud object
    def __init__(self):
        self.x = window_width + rand.randint(800, 1000)
        self.y = rand.randint(50, 100)
        # selecting image 
        self.image = clouds_images
        self.width = self.image.get_width()

    def update(self):
        # updating the position of cloud
        self.x -= game_speed
        if self.x < -self.width:
            self.x = window_width + rand.randint(2500, 3000)
            self.y = rand.randint(50, 100)

    def draw(self, SCREEN):
        #draw cloud image on screen
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = window_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = rand.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = rand.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():

    # Global Variables for game_speed, x_pos_bg, y_pos_bg, points, obstacles
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles

    # Initializing the game
    sprint = True
    clock = pg.time.Clock()

    # Creating the Dinosaur
    player = Dinosaur()

    # Creating the Clouds
    cloud = Cloud()

    # Set the game speed, x_pos_bg, y_pos_bg, points, obstacles
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []

    # Load the font
    font = pg.font.Font('freesansbold.ttf', 20)

    # Death count
    death_count = 0

    # Function for score
    def score():

        # Global variables for points, game_speed
        global points, game_speed
        points += 1

        # Increasing the game speed for every 100 points
        if points % 100 == 0:
            game_speed += 1

        # Rendering the text
        text = font.render("Points: " + str(points), True, (0, 0, 0))

        # Displaying the text
        textRect = text.get_rect()
        textRect.center = (1000, 40)

        # Blit the text to the screen
        SCREEN.blit(text, textRect)

    # Function for background
    def background():

        # Global variables for x_pos_bg, y_pos_bg
        global x_pos_bg, y_pos_bg

        # Loading the background image
        image_width = BG.get_width()

        # Blit the background image twice
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))

        # Moving the background image
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0

        # Moving the background image
        x_pos_bg -= game_speed


    # Game Loop
    while sprint:

        # Event Loop
        for event in pg.event.get():
            
            # Listening for the quit event
            if event.type == pg.QUIT:
                sprint = False

        # Fill the screen with white color
        SCREEN.fill((255, 255, 255))

        # Get the user input
        userInput = pg.key.get_pressed()

        # Draw the Dinosaur
        player.draw(SCREEN)

        # Update the Dinosaur
        player.update(userInput)

        # Create the obstacles
        if len(obstacles) == 0:
            if rand.randint(0, 2) == 0:
                obstacles.append(SmallCactus(tiny_cactus))
            elif rand.randint(0, 2) == 1:
                obstacles.append(LargeCactus(large_cactus))
            elif rand.randint(0, 2) == 2:
                obstacles.append(Bird(birds_images))

        # Draw the obstacles
        for obstacle in obstacles:

            # Draw the obstacles
            obstacle.draw(SCREEN)
            obstacle.update()

            # Collision detection
            if player.dino_rect.colliderect(obstacle.rect):
                pg.time.delay(2000)
                death_count += 1

                # Call the menu function
                menu(death_count)

        # Calling the background function for drawing and moving the background image
        background()

        # Drawing and moving the clouds
        cloud.draw(SCREEN)
        cloud.update()

        # Calling the score function
        score()

        # Updating the display
        # Clock tick 30 frames per second
        clock.tick(30)

        # Updating the display
        pg.display.update()


# Function for displaying the menu
def menu(death_count):

    # Global variables for points
    global points

    # Initializing the game
    sprint = True

    # Game Loop
    while sprint:

        # Fill the screen with white color
        SCREEN.fill((255, 255, 255))
        font = pg.font.Font('freesansbold.ttf', 30)

        # Displaying the text
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            
            # Displaying the score
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (window_width // 2, window_height // 2 + 50)
            SCREEN.blit(score, scoreRect)
        
        
        textRect = text.get_rect()
        textRect.center = (window_width // 2, window_height // 2)

        # Blit the text to the screen
        SCREEN.blit(text, textRect)

        # Blit to display the running dinosaur
        SCREEN.blit(sprinting_animation[0], (window_width // 2 - 20, window_height // 2 - 140))
        pg.display.update()

        # Event Loop
        for event in pg.event.get():

            # Listening for the quit event
            if event.type == pg.QUIT:
                sprint = False
            # Listening for the key press event
            if event.type == pg.KEYDOWN:
                main()


menu(death_count=0)
