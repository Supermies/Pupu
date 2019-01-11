import pygame, time
from random import randint, shuffle, randrange
#import numpy as np
#bunnyImg = pygame.image.load('pupu.jpg')
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
DARK = (0, 100, 0)
RED = (255, 0, 0)
BROWN = (150, 100, 0)

colour = (WHITE, BLACK, RED, BROWN)
counter = 1
N = 60

def world():
    world = {}
    positions = []
    posx = [x for x in range(0, N)]
    posy = [y for y in range(0, N)]
    for x in posx:
        for y in posy:
            world[(x, y)] = None
    return world



class Pupu():
    """A class representing a single pupu"""
    def __init__(self, colour, age, name):
        """bunnies colour and age"""
        self.colour = colour
        self.age = age
        self.name = name
        self.sex = randint(0,1)
        self.death = 10 + randint(1,4)
        self.moved = 0

    def aging(self):
        age = self.age
        self.age += 1
        return self.age + 1

    # def pupu_move(self):
    #     global positions
    #     newx = self.x + randrange(-1, 2)
    #     newy = self.y + randrange(-1, 2)
    #     newpos = (newx, newy)
    #     print((self.x, self.y))
    #     print(newpos)
    #     if newpos in positions:
    #         positions = [pos for pos in positions if pos != newpos]
    #         positions.append((self.x, self.y))
    #         self.x = newpos[0]
    #         self.y = newpos[1]
    # def __str__(self):
    #     return "bunny number:" + str(self.name)

# class Puput:
#
#     def __init__(self):
#         self.puput = [] # start with an empty list
#         global counter
#         global positions
#         positions = posishuffle(positions)
#         for i in range(10):
#             xy = positions.pop()
#             self.puput.append(Pupu(colour[randint(0,3)],0,counter,xy[0], xy[1]))
#             counter += 1
#
#     def lisapupu(self,numbunnies,positions):
#         global counter
#         collision = True
#         positions = posishuffle(positions)
#         for i in range(0,numbunnies):
#             xy = positions.pop()
#             self.puput.append(Pupu(colour[randint(0,3)],0,counter,xy[0], xy[1]))
#             # bunnylist.append((newx,newy))
#             counter += 1
#
#
#     def shuffle(self):
#         shuffle(self.puput)


#
# def kill_bunnies():
#     i = 0
#     for pupu in world.puput:
#         i += 1
#         pupu.aging()
#         if pupu.age == pupu.death:
#             print("pupu number: " + str(pupu.name) + " has died")
#             print("it was " + str(pupu.age) + " years old")
#             xy = (pupu.x, pupu.y)
#             del world.puput[i-1]
#             positions.append(xy)
#
# def make_bunnies(pupu):
#     # males = 0
#     # females = 0
#     # global positions
#     # for pupu in world.puput:
#     #     if pupu.age > 1:
#     #         if pupu.sex == 1:
#     #             males += 1
#     #         else:
#     #             females += 1
#     # if males > 0:
#     #     world.lisapupu(females,positions)
#     newpos = [(self.x - 1, self.y),(self.x + 1, self.y), (self.x, self.y - 1), (self.x, self.y + 1)]
#     newbunny = 1
#     while newbunny:
#         for i in newpos:
#             if i in positions:
#                 positions = [pos for pos in positions if pos != i]


#
# def kill_half():
#     i = 0
#     for pupu in world.puput:
#         i += 1
#         kill = randint(0,1)
#         if kill == True:
#             xy = (pupu.x, pupu.y)
#             del world.puput[i-1]
#             positions.append(xy)

def initial_bunny():
    global counter
    x = randint(0, N - 1)
    y = randint(0, N - 1)
    world[(x, y)] = Pupu(colour[randint(0,3)],0,counter)
    counter += 1

def new_bunny(row, column):
    global counter
    if world[(row-1, column)] == None:
        world[(row-1, column)] = Pupu(colour[randint(0,3)],0,counter)
        counter += 1
    elif world[(row+1, column)] == None:
        world[(row+1, column)] = Pupu(colour[randint(0,3)],0,counter)
        counter += 1
    elif world[(row, column-1)] == None:
        world[(row, column-1)] = Pupu(colour[randint(0,3)],0,counter)
        counter += 1
    elif world[(row, column)+1] == None:
        world[(row, column+1)] = Pupu(colour[randint(0,3)],0,counter)
        counter += 1

def adjacent_make_bunnies(row, column):
    if world[(row, column)].sex == 1:
        if world[(row-1, column)] and world[(row-1, column)].sex == 0:
            new_bunny(row, column)
        elif world[(row+1, column)] and world[(row-1, column)].sex == 0:
            new_bunny(row, column)
        elif world[(row, column-1)] and world[(row, column-1)].sex == 0:
            new_bunny(row, column)
        elif world[(row, column+1)] and world[(row, column+1)].sex == 0:
            new_bunny(row, column)

def adjacent_move_bunnies(row, column, free_positions):
    for i in range(len(free_positions)):
        if world[free_positions[i]] == None:
            world[free_positions[i]] = world[row, column]
            world[row, column] = None

def free_positions():
    adjacent_positions = [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]
    if row == 0:
        adjacent_positions.remove((row-1, column))
    if row == N - 1:
        adjacent_positions.remove((row+1, column))
    if column == 0:
        adjacent_positions.remove((row, column-1))
    if column == N - 1:
        adjacent_positions.remove((row, column+1))
    shuffle(adjacent_positions)
    return adjacent_positions

# Define some colors

#Grid
w = 10
h = 10
m = 1

world = world()
for i in range(0,100):
    initial_bunny()
pygame.init()

# Set the width and height of the screen [width, height]
size = ((N * w + N * m + m), (N * h + N * m + m))
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
while True:
    start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.

    screen.fill(DARK)
        # Draw the grid
    for row in range(N):
        for column in range(N):
            color = GREEN
            if world[(row, column)]:
                color = world[(row, column)].colour
            pygame.draw.rect(screen,
                             color,
                             [(m + w) * column + m,
                              (m + h) * row + m,
                              w,
                              h])
    for row in range(N):
        for column in range(N):
            positions = free_positions()
            if world[(row, column)]:
        #        adjacent_make_bunnies(row, column)
                if world[(row, column)].moved == 1:
                    world[(row, column)].moved = 0
                else:
                    world[(row, column)].moved = 1
                    adjacent_move_bunnies(row, column, positions)
    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.

    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(24)

# Close the window and quit.
    #time.sleep(0.1)

    end = time.time()
    print(1 / (end - start))
pygame.quit()
