import pygame, time, inspect
from random import randint, shuffle, randrange
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import math

#import numpy as np
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
DARK = (0, 100, 0)
DARKBROWN = (100, 80, 0)
BROWN = (150, 100, 0)
GREY = (200, 200, 200)

bunnyvalk = pygame.image.load('valkpupu.png')
bunnyrusk = pygame.image.load('ruskpupu.png')
bunnytumru = pygame.image.load('tumrupupu.png')
bunnytapla = pygame.image.load('taplapupu.png')

susi = pygame.image.load('susi.png')




north = 0
south = 0
east = 0
west = 0
bunny_count = 0
turn_counter = 1

colour = (bunnyvalk, bunnyrusk, bunnytumru, bunnytapla)
counter = 1
N = 80
area_size = N / 10

def world():
    world = {}
    #positions = []
    posx = [x for x in range(0, N)]
    posy = [y for y in range(0, N)]
    for x in posx:
        for y in posy:
            world[(x, y)] = None
    return world

def bunnies_area():
    bunnies_area = {}
    posx = [x for x in range(0, int(area_size))]
    posy = [y for y in range(0, int(area_size))]
    for x in posx:
        for y in posy:
            bunnies_area[(x, y)] = 0
    return bunnies_area



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

class Susi():
    """A class representing a single pupu"""
    def __init__(self, age, name, mother, father):
        """bunnies colour and age"""
        self.colour = susi
        self.age = age
        self.name = name
        self.mother = mother
        self.father = father
        self.sex = randint(0,1)
        self.death = 2160 + randint(1,920)
        self.moved = 0
        self.eaten = 0
        self.days_sense_eaten = 0

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

# def point_make_bunny(row, column):
#     global counter
#     world[(row, column)] = Pupu(colour[randint(0,3)],0,counter,counter,counter)
#     counter += 1

def point_make_bunny(row, column):
    global counter
    world[(row, column)] = Susi(0,counter,counter,counter)
    counter += 1

def adjacent_make_bunnies(row, column, free_positions):
    make_bunny = False
    new_bunny_position = ()
    global counter
    for i in range(len(free_positions)):
        if world[free_positions[i]] == None:
            new_bunny_position = free_positions[i]
        elif isinstance(world[free_positions[i]], Pupu) and world[free_positions[i]].sex == 0 and world[free_positions[i]].age > 180 and world[free_positions[i]].father != world[(row, column)].father and world[free_positions[i]].mother != world[(row, column)].mother and world[free_positions[i]].mother != world[(row, column)].name and world[free_positions[i]].name != world[(row, column)].father:
            make_bunny = True
            father = world[free_positions[i]].name
    if make_bunny and new_bunny_position:
        world[new_bunny_position] = Pupu(world[(row, column)].colour,0,counter,world[(row, column)].name,father)
        counter += 1

def adjacent_make_wolfies(row, column, free_positions):
    make_wolfie = False
    new_wolfie_position = ()
    global counter
    for i in range(len(free_positions)):
        if world[free_positions[i]] == None:
            new_wolfie_position = free_positions[i]
        elif isinstance(world[free_positions[i]], Susi) and world[free_positions[i]].sex == 0 and world[free_positions[i]].age > 800 and world[free_positions[i]].father != world[(row, column)].father and world[free_positions[i]].mother != world[(row, column)].mother and world[free_positions[i]].mother != world[(row, column)].name and world[free_positions[i]].name != world[(row, column)].father:
            make_wolfie = True
            father = world[free_positions[i]].name
    if make_wolfie and new_wolfie_position:
        world[new_wolfie_position] = Susi(0,counter,world[(row, column)].name,father)
        counter += 1

def adjacent_move_bunnies(row, column, free_positions):
    for i in range(len(free_positions)):
        if world[free_positions[i]] == None:
            world[free_positions[i]] = world[row, column]
            world[row, column] = None
            break
    world[(row, column)] = None

def adjacent_move_wolfies(row, column, free_positions, pref_dir):
    if range(len(free_positions)) == 0:
        world[row, column] = None
    for i in range(len(free_positions)):
        if world[free_positions[i]] == None or isinstance(world[free_positions[i]], Pupu):

            if isinstance(world[free_positions[i]], Pupu):
                # wolf = world[(row, column)].name
                # bunny = world[free_positions[i]].name
                # print("wolf {} ate bunny {}".format(wolf, bunny))
                world[row, column].days_sense_eaten = 0
                world[free_positions[i]] = world[row, column]
                world[row, column] = None
                break

            elif i == len(free_positions) - 1:

                world[row, column].days_sense_eaten += 1
                world[free_positions[i]] = world[row, column]
                world[row, column] = None
                break

            elif len(free_positions) == 4 and not pref_dir == 5:
                adjacent_positions = [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]
                if world[adjacent_positions[pref_dir]] == None or isinstance(world[adjacent_positions[pref_dir]], Pupu):
                    world[adjacent_positions[pref_dir]] = world[row, column]
                    world[row, column] = None
                break




def free_positions(row, column):
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

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def list_bunny_areas(pos):
    global area
    closest_area = ()
    for area_part in area:
        if area[area_part] > 25:
            if closest_area:
                pos_x = area_part[0] - int(pos[0]/10)
                pos_y = area_part[1] - int(pos[1]/10)
                distance_area_part = math.sqrt(abs(pos_x)^2 + abs(pos_y)^2)
                if distance_area_part < distance:
                    distance = distance_area_part
                    closest_area = area_part
            else:
                closest_area = area_part
                pos_x = closest_area[0] - int(pos[0]/10)
                pos_y = closest_area[1] - int(pos[1]/10)
                distance = math.sqrt(abs(pos_x)^2 + abs(pos_y)^2)

    if closest_area:

        pos_x = closest_area[0] - int(pos[0]/10)
        pos_y = closest_area[1] - int(pos[1]/10)
        if abs(pos_x) > abs(pos_y):
            if pos_x > 0:
                return 1
            else:
                return 0
        else:
            if pos_y < 0:
                return 2
            else:
                return 3


def poscalc(poschunk):
    global world
    global bunny_count
    global north
    global south
    global east
    global west
    global area
    for pos in poschunk:
        if world[(pos[0], pos[1])] and world[(pos[0], pos[1])].age <= world[(pos[0], pos[1])].death:
            if isinstance(world[(pos[0], pos[1])], Pupu):
                bunny_count += 1


                area[(pos[0]//10,pos[1]//10)] += 1


                if pos[0] > N / 2:
                    south += 1
                else:
                    north += 1
                if pos[1] > N / 2:
                    east += 1
                else:
                    west += 1
                if bunny_death == 1:
                    if world[(pos[0], pos[1])] and world[(pos[0], pos[1])].age > 180:
                        kill_bunny = randint(0,1)
                        if kill_bunny > 0 and world[(pos[0], pos[1])].age > 100:
                            world[(pos[0], pos[1])].death -= 400
            world[(pos[0], pos[1])].aging()
            if world[(pos[0], pos[1])].moved == 1:
                world[(pos[0], pos[1])].moved = 0
            else:
                world[(pos[0], pos[1])].moved = 1
                if isinstance(world[(pos[0], pos[1])], Pupu):
                    if world[(pos[0], pos[1])].sex == 1 and world[(pos[0], pos[1])].age > 180:
                        positions = free_positions(pos[0], pos[1])
                        adjacent_make_bunnies(pos[0], pos[1], positions)
                    positions = free_positions(pos[0], pos[1])
                    adjacent_move_bunnies(pos[0], pos[1], positions)
                if isinstance(world[(pos[0], pos[1])], Susi):
                    #print(world[(pos[0], pos[1])].days_sense_eaten)

                    if world[(pos[0], pos[1])].days_sense_eaten > 360:
                        wolf = world[(pos[0], pos[1])].name
                        #print("wolf {} starved to death".format(wolf))
                        world[(pos[0], pos[1])] = None

                    else:
                        if world[(pos[0], pos[1])].sex == 1 and world[(pos[0], pos[1])].age > 800 and world[(pos[0], pos[1])].days_sense_eaten < 60:
                            positions = free_positions(pos[0], pos[1])

                            adjacent_make_wolfies(pos[0], pos[1], positions)
                        positions = free_positions(pos[0], pos[1])

                        dir = list_bunny_areas(pos)
                        if dir == None:
                            dir = 5
                        adjacent_move_wolfies(pos[0], pos[1], positions, dir)


        elif world[(pos[0], pos[1])] and world[(pos[0], pos[1])].age > world[(pos[0], pos[1])].death:
            world[(pos[0], pos[1])] = None
# Define some colors

#Grid
w = 14
h = 14
m = 1

world = world()

worldpos = list(world.keys())
#make initial bunnies
for i in range(0,100):
    initial_bunny()

pygame.init()

# Set the width and height of the screen [width, height]
size = ((N * w + N * m + m), (N * h + N * m + m))
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")
bunnyvalk = pygame.image.load('valkpupu.png').convert_alpha()
bunnyrusk = pygame.image.load('ruskpupu.png').convert_alpha()
bunnytumru = pygame.image.load('tumrupupu.png').convert_alpha()
bunnytapla = pygame.image.load('taplapupu.png').convert_alpha()

susi = pygame.image.load('susi.png').convert_alpha()

# Loop until the user clicks the close button.
done = False
bunny_death = 0
start = time.time()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
while True:
    # y_pos = {}
    # for i in range(721):
    #      y_pos[(i)] = 0


    #start = time.time()
    area = bunnies_area()

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
           # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (w + m)
            row = pos[1] // (h + m)
            point_make_bunny(row, column)
            #print("Click ", pos, "Grid coordinates: ", row, column)



    screen.fill(DARK)
        # Draw the grid
    shuffle(worldpos)
    #
    for pos in worldpos:
        color = DARK
        if world[(pos[0], pos[1])]:
            screen.blit(world[(pos[0], pos[1])].colour,(pos[1] * (m + w), pos[0] * (m + h)))

    north = 0
    south = 0
    east = 0
    west = 0
    bunny_count = 0
    threads = []
    for poschunk in chunks(worldpos, 3200):
        process = Thread(target=poscalc, args=[poschunk])
        process.start()
        threads.append(process)
    for process in threads:
        process.join()

    #print(bunny_count)
    #print(north, south, west, east)
    if bunny_count > 1000:
        bunny_death = 1
    else:
        bunny_death = 0

    #print(area)

    pygame.display.flip()
    # turn_counter += 1
    # if turn_counter == 100:
    #     turn_counter = 0
    #     end = time.time()
    #     print(100/(end - start))
    #     start = time.time()
    #print(len(worldpos))
pygame.quit()
