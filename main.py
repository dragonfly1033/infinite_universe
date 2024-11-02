import pygame as pg
from enum import Enum
import random
from universe import Universe

class ScreenType(Enum):
    Universe = 1
    SolarSystem = 2
    Planet = 3


pg.init()


def switch_screen_callback(new_screen_type, seed):
    pass


W, H = 1880, 1000
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()
global_seed = 27

random.seed(global_seed)

universe_screen = Universe(ScreenType.Universe, global_seed, W, H)
universe_screen.setup()

active_screen = universe_screen

run = True
while run:
    dt = clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        active_screen.event_loop(event, dt) 

    active_screen.game_loop()

    display.blit(active_screen.get_surface(), (0,0))
    pg.display.update()
pg.quit()