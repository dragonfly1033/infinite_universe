import math
import random
import pygame as pg
import numpy as np
from numba import njit
from perlin_noise import PerlinNoise
from sys import exit

pg.init()

WIDTH = 1000 #1900
HEIGHT = 700 #1000
WHITE = (255, 255, 255)
seed = 60
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("TerrainGen")


points = []
rows = 20 # so 11 sets of points
cols = 20 # so 5 sets of point

the = 0
fov = 90
noise = PerlinNoise(octaves=2)
# noise = np.vectorize(noise)

for row in range(0, rows + 1) : # as each row has row+1 lines
    for col in range(0, cols + 1): # as each column has column+1 lines
        x_val = -1 + col * 2/(cols)
        z_val = 1 - row * 2/(rows)
        y_val = noise((row/rows, col/cols))
        points.append([x_val, y_val, z_val, 1])

# print(points)
# print(len(points))
points_3d = np.array(points).reshape((rows + 1,cols + 1,4))


# print("\ninitial points : ")
# print(points)
# print(len(points))
# print("\n")

# cube:
cube_points = [
    [-0.5, 0.5, 0.5, 1],
    [0.5, 0.5, 0.5, 1],
    [-0.5, -0.5, 0.5, 1],
    [0.5, -0.5, 0.5, 1],

    [0.5, -0.5, -0.5, 1],
    [-0.5, -0.5, -0.5, 1],
    [-0.5, 0.5, -0.5, 1],
    [0.5, 0.5, -0.5, 1]
]

def getProjection(xtheta, ytheta, ztheta, fov):
    X = xtheta * math.pi/180
    Y = ytheta * math.pi/180
    Z = ztheta * math.pi/180
    rotation_matrix_y = np.array([
        [math.cos(Y),   0,              math.sin(Y),  0],
        [0,             1,              0           , 0],
        [-math.sin(Y),  0,              math.cos(Y),  0],
        [0,             0,              0,            1]
    ])

    rotation_matrix_z = np.array([
        [math.cos(Z),   math.sin(Z),         0, 0],
        [-math.sin(Z),  math.cos(Z),         0, 0],
        [0,             0,                   1, 0],
        [0,             0,               0,      1]
    ])

    rotation_matrix_x = np.array([
        [1,    0,               0,              0],
        [0,    math.cos(X),     -math.sin(X),   0],
        [0,    math.sin(X),     math.cos(X),    0],
        [0,    0,               0,              1]
    ])

    a = HEIGHT/WIDTH # aspect ratio
    f = 1/math.tan(math.pi/180 * fov/2) # getting angle to screen
    zfar = -20 # furthest can see
    znear = 0.2 # closest can see
    q = zfar/(zfar - znear) # part of projection matrix, to simplify later on

    show_matrix = np.array([
        [a*f, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, q, 1],
        [0, 0, -q*znear, 0]
    ])

    # rotation_matrix = np.matmul(np.matmul(rotation_matrix_x, rotation_matrix_y), rotation_matrix_z)
    # projection_matrix = np.matmul(rotation_matrix, show_matrix)

    projection_matrix = show_matrix
    return projection_matrix

def project_3d_to_2d(points_3d, projection_matrix, xMov, yMov, zMov):
    npoints = points_3d.copy().reshape(-1, 4)
    # translating it depeneding on camera movement
    npoints[:, 0] += xMov
    npoints[:, 1] += yMov
    npoints[:, 2] += zMov

    npoints = npoints.T # transposing so can matrix multiply

    result = np.matmul(projection_matrix, npoints).T # multiplying then transposing again to get form wanted

    # dividing each element by 3rd value which should be z to get correct projected x,y vals, if z is zero then does'nt divide
    divisors = result[:, 2][:, np.newaxis]
    projected_points_2d = np.where(divisors != 0, result / divisors, result)

    projected_points_2d = projected_points_2d[:, :-2] # discarding last two elements of each array

    return projected_points_2d.reshape((rows + 1,cols + 1, 2))

def transform(x, y):
    x_val = (x + 1) / 2 * WIDTH
    y_val = HEIGHT / -2 * (y - 1)

    return [x_val, y_val]

def indexExists(i, j):
    val = i*rows + j
    if val < len(points_2d) and val > 0:
        return True
    return False

def getCoords(row, col):
    point = points_2d[row][col]
    # now need to change to screen dimensions
    return transform(point[0], point[1])

def drawTriangle(p1, p2, p3):
    pg.draw.line(screen, "white",p1, p2)
    pg.draw.line(screen, "white", p2, p3)
    pg.draw.line(screen, "white", p3, p1)

def drawPoints(): 
    global points_2d
    global the
    global fov

    # the =  (the + 1) % 360
    # fov = (fov + 1) % 400 + 1

    projection_matrix = getProjection(0, 0, 0, fov)
    points_2d = project_3d_to_2d(points_3d, projection_matrix, 0, -0.75, 0.5)

    dot_colour = "red"
    for row in range(0, rows) : # don't want to make lines for last row
        for col in range(0, cols) : # don't want to make lines for last col
            point = getCoords(row, col)
            # pg.draw.circle(screen, dot_colour,  point, 5)

            pg.draw.line(screen, "white", point, getCoords(row, col + 1))
            pg.draw.line(screen, "white", point, getCoords(row + 1, col))
            pg.draw.line(screen, "white", point, getCoords(row + 1, col + 1))


            # v = input("enter")
            # pg.display.update()

    for col in range(0, cols) :
        point = getCoords(rows, col)
        # pg.draw.circle(screen, dot_colour,  point, 5)
        pg.draw.line(screen, "white", point, getCoords(rows, col + 1))
        
    for row in range(0, rows) :
        point = getCoords(row, cols)
        # pg.draw.circle(screen, dot_colour,  point, 5)
        pg.draw.line(screen, "white", point, getCoords(row + 1, cols))
        

    # projection_matrix = getProjection(0, 0, 0, fov)
    # points_2d = project_3d_to_2d(np.array(cube_points), projection_matrix, 0, 0, 0)
    # for point in points_2d:
    #     pg.draw.circle(screen, "blue", transform(point[0], point[1]), 5)


while True:
    for event in pg.event.get():
        line_colour = "white"
       
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill("black")
    drawPoints()
    pg.display.update()
    clock.tick(60)





"""
! CHANGE TO THIS FORMAT
pg.init()
class Terrain:
    def __init__(self, type):
            pass

        def event_loop(self, event, dt):
            if event.type == pg.KEYDOWN:
                # if event.key == pg.K_a
                pass
        
        def game_loop(self):
            pass

        def get_surface(self) -> pg.Surface:
            pass

"""