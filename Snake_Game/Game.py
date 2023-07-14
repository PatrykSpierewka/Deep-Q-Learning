import pygame
import sys
import random
import gym
import math
import time
import numpy as np

WINDOWWIDTH = 200.0
WINDOWHEIGHT = 200.0
GRIDDIMENSION = 20.0

GRIDWIDTH = WINDOWWIDTH/GRIDDIMENSION
GRIDHEIGHT = WINDOWHEIGHT/GRIDDIMENSION

rectcolour0 = (50, 50, 50)
rectcolour1 = (5, 5, 5)
pygame.display.set_caption("SNAKE FOR DQN")

def dispGrid(window):
    for cord0 in range(0, int(GRIDHEIGHT)):
        for cord1 in range(0, int(GRIDWIDTH)):
            if (cord0+cord1) % 2 == 0:
                rect0 = pygame.Rect((cord1 * GRIDDIMENSION, cord0 * GRIDDIMENSION), (GRIDDIMENSION, GRIDDIMENSION))
                pygame.draw.rect(window, rectcolour0, rect0)

            else:
                rect1 = pygame.Rect((cord1 * GRIDDIMENSION, cord0 * GRIDDIMENSION), (GRIDDIMENSION, GRIDDIMENSION))
                pygame. draw.rect(window, rectcolour1, rect1)

pygame.init()
clock = pygame.time.Clock()
score = 0
FPS = 5
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
window = pygame.Surface(screen.get_size())
window = window.convert()
dispGrid(window)

SLEEP = 0.15

class Snake(gym.Env):
    def __init__(self, human = False, env_info={"state_space":None}):
        super(Snake, self).__init__()

        self.done = False
        self.temp_wall = False
        self.temp_apple = False
        self.temp_body = False
        self.len = 1
        self.position = [((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
        self.color = (105, 150, 5)
        self.first_tuple_elements_x = []
        self.first_tuple_elements_y = []
        self.score = 0

        self.reward = 0
        self.action_space = 4
        self.state_space = 112
        self.total = 0
        self.maximum = 0
        self.human = human
        self.env_info = env_info
        self.snake_body = []
        self.snake_x = []
        self.snake_y = []
        self.snake_xsc = []
        self.snake_ysc = []
        self.window_pixel_matrix = []

        self.apple_position = (0, 0)
        self.apple_color = (242, 12, 12)
        self.apple_randomPos()
        self.apple_x = []
        self.apple_y = []
        self.apple_xsc = []
        self.apple_ysc = []
        self.dist = math.sqrt((self.position[0][0] - self.apple_position[0])**2 + (self.position[0][1] - self.apple_position[1])**2)

    def checkHeadPosition(self):
        return self.position[0]

    def apple_randomPos(self):
        while True:
            self.apl_x = random.randrange(0, 180, 20)
            self.apl_y = random.randrange(0, 180, 20)
            if len(list(filter(lambda x: x == (self.apl_x, self.apl_y), self.position))) > 0:
                continue
            else:
                break
        self.apple_position = (self.apl_x, self.apl_y)
        return (self.apl_x, self.apl_y)


    def turn(self, x, y):
        if self.len > 1 and (x * -1, y * -1) == self.direction:
            return
        else:
            self.direction = x, y

    def move_snake(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.turn(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.turn(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.turn(1, 0)

        self.curv = self.checkHeadPosition()
        self.startx, self.starty = self.direction
        self.start = (((self.curv[0] + (self.startx * GRIDDIMENSION)) % WINDOWWIDTH), (self.curv[1] + (self.starty * GRIDDIMENSION)) % WINDOWHEIGHT)

        if len(self.position) > 2 and self.start in self.position[2:]:
            self.temp_body = True
            self.len = 1
            self.position = [((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))]
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        else:
            self.position.insert(0, self.start)
            self.temp_apple = False
            if len(self.position) > self.len:
                self.position.pop()

        if (self.direction == (1, 0) and self.position[0][0] == 0.0) or (
                self.direction == (-1, 0) and self.position[0][0] == WINDOWWIDTH - 20.0) or (
                self.direction == (0, 1) and self.position[0][1] == 0.0) or (self.direction == (0, -1) and self.position[0][1] == WINDOWHEIGHT - 20.0):
            self.temp_wall = True
            self.len = 1
            self.position = [((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))]
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def move_apple(self):
        if self.checkHeadPosition() == self.apple_position:
            self.temp_apple = True
            self.len += 1
            if self.len + 1:
                self.score += 1
                # print("Wynik {0}".format(self.score))
            self.apple_randomPos()

    def display_snake(self, window):
        for x in self.position:
            rect0 = pygame.Rect((x[0], x[1]), (GRIDDIMENSION, GRIDDIMENSION))
            pygame.draw.rect(window, self.color, rect0)
            #pygame.draw.rect(window, (255, 255, 255), rect0)

    def display_apple(self, window):
        rect0 = pygame.Rect(self.apple_position, (GRIDDIMENSION, GRIDDIMENSION))
        pygame.draw.rect(window, self.apple_color, rect0)

    def measure_distance(self):
        self.prev_dist = self.dist
        self.dist = math.sqrt((self.position[0][0] - self.apple_position[0])**2 + (self.position[0][1] - self.apple_position[1])**2)

    def reset(self):
        #time.sleep(1)
        self.len = 1
        self.position = [((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.reward = 0
        self.score = 0
        self.total = 0
        self.temp_wall = False
        self.temp_body = False
        self.done = False
        state = self.get_state()
        return state

    def board_or_body_check(self):
        window_pixel_matrix = pygame.transform.scale(window, (10, 10))
        window_pixel_matrix = pygame.surfarray.array3d(window_pixel_matrix)

        check_values = np.array([105, 150, 5])
        apple_color = np.array([242, 12, 12])
        binary_array = []

        for i in range(10):
            for j in range(10):
                pixel_color = window_pixel_matrix[:, :, 0][i][j]
                if np.array_equal(pixel_color, check_values):
                    binary_array.append(1)
                elif np.array_equal(pixel_color, apple_color):
                    binary_array.append(0.5)
                else:
                    binary_array.append(0)

        return binary_array

    def run_game(self):
        reward_given = False
        screen.blit(window, (0, 0))
        pygame.display.update()
        dispGrid(window)

        self.move_snake()
        self.move_apple()
        self.measure_distance()
        self.display_snake(window)
        self.display_apple(window)
        self.board_or_body_check()


        if self.temp_body:
            self.reward = -100
            reward_given = True
            self.done = True
            if self.human:
                self.reset()

        if self.temp_apple:
            self.reward = 10
            reward_given = True

        if self.temp_wall:
            self.reward = -100
            reward_given = True
            self.done = True
            if self.human:
                self.reset()

        if self.human:
            time.sleep(SLEEP)
            pass


    def step(self, action):
        if action == 0:
            self.turn(0, -1)
        if action == 1:
            self.turn(1, 0)
        if action == 2:
            self.turn(0, 1)
        if action == 3:
            self.turn(-1, 0)

        self.run_game()
        state = self.get_state()
        return state, self.reward, self.done, {}

        if (self.direction == (1, 0) and self.position[0][0] == 0.0) or (
                self.direction == (-1, 0) and self.position[0][0] == WINDOWWIDTH - 20.0) or (
                self.direction == (0, 1) and self.position[0][1] == 0.0) or (self.direction == (0, -1) and self.position[0][1] == WINDOWHEIGHT - 20.0):
            self.temp_wall = True
            self.len = 1
            self.position = [((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))]
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def get_state(self):
        if self.direction == (0, -1):
            self.dir_up = True
        else:
            self.dir_up = False

        if self.direction == (0, 1):
            self.dir_down = True
        else:
            self.dir_down = False

        if self.direction == (1, 0):
            self.dir_right = True
        else:
            self.dir_right = False

        if self.direction == (-1, 0):
            self.dir_left = True
        else:
            self.dir_left = False

        if self.apple_position[1] < self.position[0][1]:
            self.apl_up = True
        else:
            self.apl_up = False

        if self.apple_position[1] > self.position[0][1]:
            self.apl_down = True
        else:
            self.apl_down = False

        if self.apple_position[0] > self.position[0][0]:
            self.apl_right = True
        else:
            self.apl_right = False

        if self.apple_position[0] < self.position[0][0]:
            self.apl_left = True
        else:
            self.apl_left = False

        if self.position[0][1] == WINDOWHEIGHT - 40.0:
            self.wall_up = True
        else:
            self.wall_up = False

        if self.position[0][1] == 20.0:
            self.wall_down = True
        else:
            self.wall_down = False

        if self.position[0][0] == 20.0:
            self.wall_right = True
        else:
            self.wall_right = False

        if self.position[0][0] == WINDOWWIDTH - 40.0:
            self.wall_left = True
        else:
            self.wall_left = False

        state = [self.apl_up, self.apl_down, self.apl_right, self.apl_left, self.dir_up, self.dir_down, self.dir_right, self.dir_left, self.wall_up, self.wall_down, self.wall_right, self.wall_left] + list(self.board_or_body_check())
        return state

if __name__ == '__main__':
    human = True
    env = Snake(human=human)

    if human:
        while True:
            env.run_game()
