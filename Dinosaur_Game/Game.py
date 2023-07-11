import random
import gym
import pygame
import os
import sys
import time

pygame.init()
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Textures/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Textures/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Textures/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Textures/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Textures/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Textures/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Textures/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Textures/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Textures/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Textures/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Textures/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Textures/Other", "Track.png"))

userInput = pygame.key.get_pressed()
clock = pygame.time.Clock()
SLEEP = 0.08

class Dinosaur(gym.Env):
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 5.8
    def __init__(self, human = False):
        super(Dinosaur, self).__init__()

        self.done = False
        self.reward = 0
        self.human = human

        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.x_cloud = SCREEN_WIDTH + random.randint(800, 1000)
        self.y_cloud = random.randint(50, 100)
        self.image_cloud = CLOUD
        self.width_cloud = self.image.get_width()

        self.image_width_bg = BG.get_width()
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.points = 0
        self.game_speed = 16*4
        self.font = font = pygame.font.Font("freesansbold.ttf", 20)

        self.obstacles = []
        self.index = 1

        self.reward = 0
        self.dist = 0

        self.action_space = 3
        self.state_space = 4
        self.observation_space = 100
        self.count = 0

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if userInput[pygame.K_UP] and self.dino_rect.y == 310:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 14
            self.jump_vel -= 1.6
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        if self.dino_rect.y > 310:
            self.dino_rect.y = 310


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def update_cloud(self):
        self.x_cloud -= self.game_speed
        if self.x_cloud < -self.width_cloud:
            self.x_cloud = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y_cloud = random.randint(50, 100)

    def draw_cloud(self, SCREEN):
        SCREEN.blit(self.image_cloud, (self.x_cloud, self.y_cloud))

    def background(self, SCREEN):
        image_width = BG.get_width()
        SCREEN.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self, SCREEN):
        self.points += 1
        text = self.font.render("Score: " + str(self.points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def obstacle_update(self):
        self.rect.x -= self.game_speed
        if self.rect.x < 12:
            self.rect.x = 0
            self.obstacles.pop()

    def obstacle_spawn(self, SCREEN):
        self.index += 1
        if self.index >= 9:
            self.index = 0

        if len(self.obstacles) == 0:
            self.type = random.randint(0, 6)

        if len(self.obstacles) == 0:
            if self.type == 0:
                self.image_obs = SMALL_CACTUS[0]
                self.rect = self.image_obs.get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.x -= self.game_speed
                self.rect.y = 325
                self.obstacles.append(SMALL_CACTUS[0])

            elif self.type == 1:
                self.image_obs = SMALL_CACTUS[1]
                self.rect = self.image_obs.get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.x -= self.game_speed
                self.rect.y = 325
                self.obstacles.append(SMALL_CACTUS[1])

            elif self.type == 2:
                self.image_obs = SMALL_CACTUS[2]
                self.rect = self.image_obs.get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.x -= self.game_speed
                self.rect.y = 325
                self.obstacles.append(SMALL_CACTUS[2])

            elif self.type == 3:
                self.image_obs = LARGE_CACTUS[0]
                self.rect = self.image_obs.get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.x -= self.game_speed
                self.rect.y = 300
                self.obstacles.append(LARGE_CACTUS[0])

            elif self.type == 4:
                self.image_obs = LARGE_CACTUS[1]
                self.rect = self.image_obs.get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.x -= self.game_speed
                self.rect.y = 300
                self.obstacles.append(LARGE_CACTUS[1])

            elif self.type == 5:
                self.image_obs = LARGE_CACTUS[2]
                self.rect = self.image_obs.get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.x -= self.game_speed
                self.rect.y = 300
                self.obstacles.append(LARGE_CACTUS[2])

            elif self.type == 6:
                self.image_obs = BIRD[self.index // 5]
                self.rect = self.image_obs.get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.y = 250
                self.obstacles.append(BIRD[self.index // 5])

        for x in self.obstacles:
            if self.type == 0 or self.type == 1 or self.type == 2 or self.type == 3 or self.type == 4 or self.type == 5:
                SCREEN.blit(x, self.rect)

            self.obstacle_update()
            if self.dino_rect.colliderect(self.rect):
                self.reset()


            if self.type == 6:
                SCREEN.blit(BIRD[self.index // 5], self.rect)

    def reset(self):
        #time.sleep(0.5)
        self.points = 0
        self.game_speed = 16*4
        self.reward = 0
        self.dino_rect.x = 80
        self.dino_rect.y = 310
        self.image = self.run_img[self.step_index // 5]
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        if len(self.obstacles) == 1:
            self.obstacles.pop()

        self.done = False
        state = self.get_state()
        return state

    def step(self, action):
        if action == 0  and self.dino_rect.y == 310:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            if self.dino_duck == False and self.dino_run == False and self.dino_jump == True:
                self.jump()

        if action == 1 and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump =  False
            if self.dino_duck == True and self.dino_run == False and self.dino_jump == False:
                self.duck()

        if action == 2 and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        if self.dino_duck == False and self.dino_run == True and self.dino_jump == False:
            self.run()

        if self.step_index >= 10:
            self.step_index = 0

        self.run_game()
        state = self.get_state()
        return state, self.reward, self.done, {}

    def measure_distance(self):
        self.prev_dist = self.dist
        self.dist = self.rect.x

    def run_game(self):
        pygame.display.update()
        reward_given = False
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        self.background(SCREEN)
        self.draw(SCREEN)
        self.draw_cloud(SCREEN)
        self.score(SCREEN)
        self.update_cloud()
        self.update(userInput)
        self.obstacle_spawn(SCREEN)
        self.measure_distance()

        if not reward_given:
            if self.dist < self.prev_dist:
                self.reward = 1

        if self.human:
            time.sleep(SLEEP)
            state = self.get_state()

    def get_state(self):
        if len(self.obstacles) == 1:
            self.normalize_x = self.rect.x / 1068
            self.normalize_y = (self.rect.y - 250) / 75
            self.normalize_dino_x = (self.dino_rect.x + self.dino_rect.width) / 1068
            self.normalize_dino_y = (self.dino_rect.y - 145) / 195
            state = [self.normalize_x, self.normalize_y, self.normalize_dino_x, self.normalize_dino_y]
        else:
            state = [0.15730337078651685, 1.0, 0.8461538461538462, 1.0]

        return state


player = Dinosaur()

if __name__ == '__main__':
    human = True
    env = Dinosaur(human=human)

    if human:
        while True:
            env.run_game()