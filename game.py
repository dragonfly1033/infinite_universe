import pygame as pg
from system import System
import pickle
from planet import Planet
from vector import Vector
from math import sin, cos, pi, sqrt, e



def getR(x):
    t1 = 30/sqrt(2*pi)
    f1 = (x-240)/90
    exp = (-1)*0.5*f1*f1
    eterm = e**exp
    fin = t1*eterm
    return fin


def getM(x):
    t1 = 1530000/sqrt(2*pi)
    f1 = (x-240)/37
    exp = (-1)*0.5*f1*f1
    eterm = e**exp
    fin = t1*eterm
    return fin


def solarSystemScreenSetup():
    solarSystemScreen.fill((0,0,0))
    pathLayer = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)



def lehmer(low, high):
    global lseed
    lseed += 0xe120fc15
    tmp = lseed * 0x4a39b70d
    m1 = (tmp >> 32) ^ tmp
    tmp = m1 * 0x12fad5c9
    m2 = (tmp >> 32) ^ tmp
    return m2%(high-low) + low



def universeScreenSetup():
    global lseed
    nSectorX = WIDTH//sectorSize
    nSectorY = HEIGHT//sectorSize
    universeScreen.fill((0,0,0))
    showing.clear()
    for y in range(nSectorY):
        for x in range(nSectorX):
            sectorX = (cX//sectorSize) + x
            sectorY = (cY//sectorSize) + y 
            px = sectorX*sectorSize - cX
            py = sectorY*sectorSize - cY
            lseed = sectorY << 16 | abs(sectorX+360)
            if lehmer(0,15) == 0:
                colour = (lehmer(0,256), lehmer(0,256), lehmer(0,256))
                r = lehmer(5,(sectorSize-1)//2)
                name = ''.join([syllables[lehmer(0,len(syllables))] for i in range(lehmer(3,7))])
                new = System(name, colour, px+(sectorSize//2), py+(sectorSize//2), r, universeScreen)
                new.plot()
                showing.append(new)
    coord = font.render(f'({cX},{cY})', False, (255,255,255))
    universeScreen.blit(coord, (0,0))


WIDTH = 1224
HEIGHT = 612

pg.init()
pg.font.init()
font = pg.font.SysFont('Calibri', 14)
display = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


cX = 0
cY = 0
lseed = 0
sectorSize = 36
vel = 4
showing = []
with open('syllables.pickle', 'rb') as f:
    syllables = pickle.load(f)


universeScreen = pg.Surface((WIDTH, HEIGHT))
universeScreenSetup()
solarSystemScreen = Screen()
solarSystemScreenSetup()


curPage = universeScreen

run = True
while run:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LSHIFT]:
        tempVel = vel*2
    elif keys[pg.K_LCTRL]:
        tempVel = vel//4
    else:
        tempVel = vel
    if keys[pg.K_w]:
        cY -= tempVel
        universeScreenSetup()
    if keys[pg.K_a]:
        cX -= tempVel
        universeScreenSetup()
    if keys[pg.K_s]:
        cY += tempVel
        universeScreenSetup()
    if keys[pg.K_d]:
        cX += tempVel
        universeScreenSetup()

    clock.tick(256)
    display.blit(curPage, (0,0))
    pg.display.update()

pg.quit()
quit()