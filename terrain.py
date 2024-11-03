import math
import random
import pygame as pg
import numpy as np
from numba import njit
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
rows = 4
cols = 3
xMultiplier = WIDTH / cols
yMultiplier = HEIGHT / rows
xOffset = xMultiplier / 2
yOffset = yMultiplier / 2

the = 0
fov = 15

for y in range(0, rows) :
    for x in range(0, cols):
        # points.append([x * xMultiplier + xOffset ,y * yMultiplier + yOffset, random.randint(-1,1) -20*y , 1])
        # points.append([x * xMultiplier + xOffset , random.randint(-20,20) + HEIGHT , -y * yMultiplier - yOffset, 1])

        x_val = -1 + x * 2/(cols-1)
        y_val = (random.random() * 2 - 1) * 0.2
        y_val = -0.5
        z_val = -1 + y * 2/(rows-1)
        points.append([x_val, y_val, z_val])
points_3d = np.array(points)

print("\ninitial points : ")
print(points)

# cube:
cube_points = [
    [-0.5, 0.5, 0.5],
    [0.5, 0.5, 0.5],
    [-0.5, -0.5, 0.5],
    [0.5, -0.5, 0.5],

    [0.5, -0.5, -0.5],
    [-0.5, -0.5, -0.5],
    [-0.5, 0.5, -0.5],
    [0.5, 0.5, -0.5]
]

def getProjection(xtheta, ytheta, ztheta, fov):
    X = xtheta * math.pi/180
    Y = ytheta * math.pi/180
    Z = ztheta * math.pi/180
    rotation_matrix_y = np.array([
        [math.cos(Y),   0,              math.sin(Y),  0],
        [0,             1,              0           , 0],
        [-math.sin(Y),  0,              math.cos(Y),  0],
        [0,             0,              0,              1]
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

    n = math.tan(math.pi/180 * fov/2) # getting angle to screen

    show_matrix = np.array([
        [n, 0, 0],
        [0, n, 0],
        [0, 0, 1],
        [0, 0, 1]
    ])

    rotation_matrix = np.matmul(np.matmul(rotation_matrix_x, rotation_matrix_y), rotation_matrix_z)
    projection_matrix = np.matmul(rotation_matrix, show_matrix)

    return projection_matrix

def project_3d_to_2d(points_3d, projection_matrix):
    npoints = points_3d.copy() # copying to then do below
    # npoints[:, 2] -= 1 # subtracting 1 from each value so can have camera at (0,0,0) and everything else around
    npoints = npoints.T # transposing so can matrix multiply

    result = np.matmul(projection_matrix, npoints).T # multiplying then transposing again to get form wanted
     # dividing each element by 3rd value to get correct projected x,y vals, if z is zero then does'nt divide
    divisors = result[:, 2][:, np.newaxis]
    projected_points_2d = np.where(divisors != 0, result / divisors, result)
    projected_points_2d = projected_points_2d[:, :-2] # discarding last two elements of each array

    return projected_points_2d

projection_matrix = getProjection(0, 0, 0, fov)
points_2d = project_3d_to_2d(points_3d, projection_matrix)
print(points_2d)

def indexExists(i, j):
    val = i*rows + j
    if val < len(points_2d):
        return True
    return False

def getCoords(row, col):
    point = points_2d[row*rows + col]
    
    # now need to change to screen dimensions
    x_val = (point[0] + 1) / 2 * WIDTH
    y_val = HEIGHT / -2 * (point[1] - 1)

    return [x_val, y_val]

# print("\ncoords of points")
# print(getCoords(1, 2), points_2d)

def drawPoints(): 
    global points_2d
    global the
    global fov

    # the =  (the + 1) % 360
    # fov = (fov + 1) % 400 + 1
    projection_matrix = getProjection(0, 0, 0, fov)
    points_2d = project_3d_to_2d(points_3d, projection_matrix)
    
    # points_2d = points_3d

    pg.draw.circle(screen, "blue", getCoords(2,2), 9)
    for row in range(0, rows) : # cols - 1 as will then need to find point next and below
        for col in range(0, cols): # rows - 1
            point = getCoords(col, row)
            # point_to_right = getCoords(i + 1, j)
            # point_to_bottom = getCoords(i, j + 1)
            pg.draw.circle(screen, "red", point, 5)

            # # drawing triangle
            # pg.draw.line(screen, line_colour, point, point_to_right)
            # pg.draw.line(screen, line_colour, point_to_right, point_to_bottom)
            # pg.draw.line(screen, line_colour, point_to_bottom, point)

            # # if at last column or row, need to draw an extra line
            # if i == cols - 2 :
            #     point_to_corner = getCoords(i + 1, j + 1)
            #     pg.draw.circle(screen, "red", point_to_corner, 5)
            #     pg.draw.line(screen, line_colour, point_to_right, point_to_corner)

            # if j == rows - 2 :
            #     point_to_corner = getCoords(i + 1, j + 1)
            #     pg.draw.circle(screen, "red", point_to_corner, 5)
            #     pg.draw.circle(screen, "red", point_to_bottom, 5)
            #     pg.draw.line(screen, line_colour, point_to_corner, point_to_bottom)


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