import pygame as pg
import os
import random as random

from dino import Dinosaur

pg.init()

# Global Constants
#Set SCREEN_VAR Dimensions
window_height = 500
window_width = 1150

# Initializing obs

tiny_cactus = [pg.image.load(os.path.join("Assets/Cactus", "SmallCactusImg1.png")),
                pg.image.load(os.path.join("Assets/Cactus", "SmallCactusImg2.png")),
                pg.image.load(os.path.join("Assets/Cactus", "SmallCactusImg3.png"))]
large_cactus = [pg.image.load(os.path.join("Assets/Cactus", "LargeCactusImg1.png")),
                pg.image.load(os.path.join("Assets/Cactus", "LargeCactusImg2.png")),
                pg.image.load(os.path.join("Assets/Cactus", "LargeCactusImg3.png"))]

birds_imgs = [pg.image.load(os.path.join("Assets/Bird", "BirdImg1.png")),
        pg.image.load(os.path.join("Assets/Bird", "BirdImg2.png"))]

clouds_imgs = pg.image.load(os.path.join("Assets/Other", "CloudImg.png"))

SCREEN_VAR = pg.display.set_mode((window_width, window_height))

sprinting_anim = [pg.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pg.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
hopping_anim = pg.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
crouching_anim = [pg.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pg.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

BG = pg.image.load(os.path.join("Assets/Other", "TrackImg.png"))

# display  clouds on the SCREEN_VAR 
class Cloud:
    #initializes new cloud object
    def __init__(obj):
        obj.x = window_width + random.randint(800, 1000)
        obj.y = random.randint(50, 100)
        # selecting image 
        obj.image = clouds_imgs
        obj.width = obj.image.get_width()

    def update(obj):
        # updating the position of cloud
        obj.x -= gspeed
        if obj.x < -obj.width:
            obj.x = window_width + random.randint(2500, 3000)
            obj.y = random.randint(50, 100)

    def draw(obj, Variable_scr):
        #draw cloud image on SCREEN_VAR
        Variable_scr.blit(obj.image, (obj.x, obj.y))


class Obstacle:
    def __init__(obj, img, type):
        obj.image = img
        obj.type = type
        obj.rect = obj.image[obj.type].get_rect()
        obj.rect.x = window_width

    def update(obj):
        obj.rect.x -= gspeed
        if obj.rect.x < -obj.rect.width:
            obs.pop()

    def draw(obj, variable_scr):
        variable_scr.blit(obj.image[obj.type], obj.rect)


class Small_cactus(Obstacle):
    def __init__(obj, img):
        obj.type = random.randint(0, 2)
        super().__init__(img, obj.type)
        obj.rect.y = 325


class Large_cactus(Obstacle):
    def __init__(obj, img):
        obj.type = random.randint(0, 2)
        super().__init__(img, obj.type)
        obj.rect.y = 300


class Bird(Obstacle):
    def __init__(obj, img):
        obj.type = 0
        super().__init__(img, obj.type)
        obj.rect.y = 250
        obj.idx = 0

    def draw(obj, Variable_scr):
        if obj.idx >= 9:
            obj.idx = 0
        Variable_scr.blit(obj.image[obj.idx//5], obj.rect)
        obj.idx += 1


def main():

    # Global Variables for gspeed, xposbg, yposbg, pts, obs
    global gspeed, xposbg, yposbg, pts, obs

    # Initializing the game
    sprint = True
    clock = pg.time.Clock()

    # Creating the Dinosaur
    dino_player = Dinosaur()

    # Creating the Clouds
    cloud = Cloud()

    # Set the game speed, xposbg, yposbg, pts, obs
    gspeed = 20
    xposbg = 0
    yposbg = 380
    pts = 0
    obs = []

    # Load the font
    font = pg.font.Font('freesansbold.ttf', 20)

    # Death count
    death_cnt = 0

    # Function for score
    def score_function():

        # Global variables for pts, gspeed
        global pts, gspeed
        pts += 1

        # Increasing the game speed for every 50 pts
        if pts % 50 == 0:
            gspeed += 1

        # Rendering the txt
        txt = font.render("Points: " + str(pts), True, (0, 0, 0))

        # Displaying the txt
        txtRect = txt.get_rect()
        txtRect.center = (1000, 40)

        # Blit the txt to the SCREEN_VAR
        SCREEN_VAR.blit(txt, txtRect)



    # Function for background
    def background_function():

        # Global variables for xposbg, yposbg
        global xposbg, yposbg

        # Loading the background image
        img_wid = BG.get_width()

        # Blit the background image twice
        SCREEN_VAR.blit(BG, (xposbg, yposbg))
        SCREEN_VAR.blit(BG, (img_wid + xposbg, yposbg))

        # Moving the background image
        if xposbg <= -img_wid:
            SCREEN_VAR.blit(BG, (img_wid + xposbg, yposbg))
            xposbg = 0

        # Moving the background image
        xposbg -= gspeed


    # Game Loop
    while sprint:

        # Event Loop
        for evnt in pg.event.get():
            
            # Listening for the quit event
            if evnt.type == pg.QUIT:
                sprint = False

        # Fill the SCREEN_VAR with white color
        SCREEN_VAR.fill((255, 255, 255))

        # Get the user input
        usrInp = pg.key.get_pressed()

        # Draw the Dinosaur
        dino_player.draw(SCREEN_VAR)

        # Update the Dinosaur
        dino_player.update(usrInp)

        # Create the obstacle
        if len(obs) == 0:
            if random.randint(0, 2) == 0:
                obs.append(Small_cactus(tiny_cactus))
            elif random.randint(0, 2) == 1:
                obs.append(Large_cactus(large_cactus))
            elif random.randint(0, 2) == 2:
                obs.append(Bird(birds_imgs))

        # Draw the obs
        for obstacle in obs:

            # Draw the obs
            obstacle.draw(SCREEN_VAR)
            obstacle.update()

            # Collision detection
            if dino_player.dino_rect.colliderect(obstacle.rect):
                pg.time.delay(2000)
                death_cnt += 1

                # Call the menu_function function
                menu_function(death_cnt)

        # Calling the background function for drawing and moving the background image
        background_function()

        # Drawing and moving the clouds
        cloud.draw(SCREEN_VAR)
        cloud.update()

        # Calling the score_function function
        score_function()

        # Updating the display
        # Clock tick 30 frames per second
        clock.tick(30)

        # Updating the display
        pg.display.update()


# Function for displaying the menu
def menu_function(death_cnt):

    # Global variables for pts
    global pts

    # Initializing the game
    sprint = True

    # Game Loop
    while sprint:

        # Fill the SCREEN_VAR with white color
        SCREEN_VAR.fill((255, 255, 255))
        font = pg.font.Font('freesansbold.ttf', 30)

        # Displaying the txt
        if death_cnt == 0:
            txt = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_cnt > 0:
            txt = font.render("Press any Key to Restart", True, (0, 0, 0))
            
            # Displaying the score
            score = font.render("Your Score: " + str(pts), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (window_width // 2, window_height // 2 + 50)
            SCREEN_VAR.blit(score, scoreRect)
        
        
        txtRect = txt.get_rect()
        txtRect.center = (window_width // 2, window_height // 2)

        # Blit the txt to the SCREEN_VAR
        SCREEN_VAR.blit(txt, txtRect)

        # Blit to display the running dinosaur
        SCREEN_VAR.blit(sprinting_anim[0], (window_width // 2 - 20, window_height // 2 - 140))
        pg.display.update()

        # Event Loop
        for evnt in pg.event.get():

            # Listening for the quit event
            if evnt.type == pg.QUIT:
                sprint = False
            # Listening for the key press evnt
            if evnt.type == pg.KEYDOWN:
                main()


menu_function(death_cnt=0)
