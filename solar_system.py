import pygame as pg
from pygame.math import Vector2 as Vec
from enum import Enum
import random

pg.init()

def rands(start, end, num, min_dist):
    if num*3 + min_dist*num < end-start:
        return []

    nums = []
    while len(nums) < num:
        r = random.randint(start, end)
        valid = True
        for i in nums:
            if abs(i-r) < min_dist:
                valid = False
                break
        if valid:
            nums.append(r)
    return nums



class SunType(Enum):
    O = {"colour": (181, 205, 255), "radius": 66}
    B = {"colour": (199,216, 255), "radius": 42}
    A = {"colour": (221,230, 255), "radius": 16}
    F = {"colour": (255,246, 237), "radius": 12}
    G = {"colour": (255,228, 206), "radius": 10}
    K = {"colour": (255,206, 166), "radius": 8}
    M = {"colour": (255,159, 70), "radius": 5}


class SolarSystem:
    def __init__(self, seed, sector_size):
        self.sector_size = sector_size
        self.max_planet_r = (self.sector_size - 2)//2
        self.min_planet_r = 5
        self.max_orbit_r = min(self.size.x, self.size.y) - self.max_planet_r - 2
        self.min_orbit_r = 66 + self.min_planet_r + 2


class GalaxyScreen:
    def __init__(self, seed, W, H):
        self.seed = seed
        self.size = Vec(W, H)
        self.sector_size = 40
        self.size = Vec(self.size.x // self.sector_size, self.size.y // self.sector_size)
        self.surf = pg.Surface((self.size.x, self.size.y))
        self.pos = Vec(0,0)

        # genrate orbits
        # calculate planet radii from orbits
        # 


    def event_loop(self, event, dt):
        if event.type == pg.KEYDOWN:
            # if event.key == pg.K_a
            pass
    
    def game_loop(self):
        pass

    def get_surface(self) -> pg.Surface:
        self.surf.fill((0,0,0))

        for j in range(self.grid_h):
            for i in range(self.grid_w):
                sector_num = self.pos//self.sector_size + Vec(x, y)
                sector_pos = sector_num*self.sector_size - self.pos
                seed = sector_num.y << 16 | abs(sector_num.x+360)
                if random.randint(0, 15) == 0:
                    r = random.randint(5, 30)
                
