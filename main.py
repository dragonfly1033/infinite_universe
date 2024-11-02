import pygame as pg
from enum import Enum
import random

class ScreenType(Enum):
    Universe = 1
    SolarSystem = 2
    Planet = 3



pg.init()


W, H = 1880, 1000
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()
global_seed = 27

random.seed(global_seed)

active_screen = None

run = True
while run:
    dt = clock.tick(60)
    if active_screen is None:
        continue

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        active_screen.event_loop(event) 

    active_screen.game_loop()

    display.blit(active_screen.get_surface(), (0,0))
    pg.display.update()
pg.quit()