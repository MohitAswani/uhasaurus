import pygame as pg
import os
pg.init()

sprinting_animation = [pg.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pg.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
hopping_animation = pg.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
crouching_animation = [pg.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pg.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

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