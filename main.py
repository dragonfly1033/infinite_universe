import pygame as pg
from enum import Enum
import random
from universe import Universe
from solar_system import GalaxyScreen

class ScreenType(Enum):
    Universe = 1
    Galaxy = 2
    Planet = 3

pg.init()

def change_screen(screen_type, seed):
    pass

W, H = 1880, 1000
display = pg.display.set_mode((W, H))
clock = pg.time.Clock()
global_seed = 27

random.seed(global_seed)

universe_screen = Universe(ScreenType.Universe, global_seed, W, H, change_screen)
universe_screen.setup()

galaxy_screen = GalaxyScreen(global_seed, W, H)

active_screen = universe_screen

run = True
while run:
    dt = clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False
                
        active_screen.event_loop(event, dt) 

    active_screen.game_loop()

    display.blit(active_screen.get_surface(), (0,0))
    pg.display.update()
pg.quit()