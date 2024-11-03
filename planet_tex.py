import numpy as np
import random, ctypes, os
from math import pi



def gen_planet_pixarray(r, seed=None):
    if seed is None:
        seed = random.randint(0, 100)
    res = round(pi * r);
    so_file = os.getcwd()+"/fast.so"
    cdll = ctypes.CDLL(so_file)
    cdll.get_image.restype = ctypes.POINTER(ctypes.c_int)
    arr = np.zeros((12*r*r+12*r+3,)).astype(np.int32)
    cols = np.zeros((6,)).astype(np.int32)
    cdll.get_image.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        np.ctypeslib.ndpointer(np.int32, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        np.ctypeslib.ndpointer(np.int32, flags="C_CONTIGUOUS"),
    ]
    out = cdll.get_image(r, res, arr, seed, cols)

    print(cols)
    return arr.reshape((2*r+1, 2*r+1, 3))

import pygame as pg

display = pg.display.set_mode((300, 300))

plan = pg.surfarray.make_surface(gen_planet_pixarray(100))
plan.set_colorkey((0,0,0))

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    display.blit(plan, (100, 100))
    pg.display.update()
pg.quit()