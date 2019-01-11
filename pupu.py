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
N = 80

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
    def __init__(self, colour, age, name, mother, father):
        """bunnies colour and age"""
        self.colour = colour
        self.age = age
        self.name = name
        self.mother = mother
        self.father = father
        self.sex = randint(0,1)
        self.death = 360 + randint(1,360)
        self.moved = 0

    def aging(self):
        age = self.age
        self.age += 1
        return self.age + 1


def initial_bunny():
    global counter
    x = randint(0, N - 1)
    y = randint(0, N - 1)
    world[(x, y)] = Pupu(colour[randint(0,3)],0,counter,counter,counter)
    counter += 1

def adjacent_make_bunnies(row, column, free_positions):
    make_bunny = False
    new_bunny_position = ()
    global counter
    for i in range(len(free_positions)):
        if world[free_positions[i]] == None:
            new_bunny_position = free_positions[i]
        elif world[free_positions[i]].sex == 0 and world[free_positions[i]].age > 26 and world[free_positions[i]].father != world[(row, column)].father and world[free_positions[i]].mother != world[(row, column)].mother and world[free_positions[i]].mother != world[(row, column)].name and world[free_positions[i]].name != world[(row, column)].father:
            make_bunny = True
            father = world[free_positions[i]].name
    if make_bunny and new_bunny_position:
        world[new_bunny_position] = Pupu(world[(row, column)].colour,0,counter,world[(row, column)].name,father)
        counter += 1

def adjacent_move_bunnies(row, column, free_positions):
    for i in range(len(free_positions)):
        if world[free_positions[i]] == None:
            world[free_positions[i]] = world[row, column]
            world[row, column] = None
    world[(row, column)] = None


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
for i in range(0,300):
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
    bunny_count = 0
    for row in range(N):
        for column in range(N):
            positions = free_positions()
            if world[(row, column)] and world[(row, column)].age <= world[(row, column)].death:
                bunny_count += 1
                world[(row, column)].aging()
                if world[(row, column)].moved == 1:
                    world[(row, column)].moved = 0
                else:
                    world[(row, column)].moved = 1
                    if world[(row, column)].sex == 1 and world[(row, column)].age > 27:
                        adjacent_make_bunnies(row, column, positions)
                    adjacent_move_bunnies(row, column, positions)
            elif world[(row, column)] and world[(row, column)].age > world[(row, column)].death:
                world[(row, column)] = None

    if bunny_count > 1000:
        for row in range(N):
            for column in range(N):
                if world[(row, column)]:
                    kill_bunny = randint(0,1)
                    if kill_bunny > 0:
                        world[(row, column)].age += 50
    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.

    pygame.display.flip()

    # --- Limit to 60 frames per second
    #clock.tick(12)

# Close the window and quit.
    #time.sleep(2)

    end = time.time()
    #print(1 / (end - start))
pygame.quit()
