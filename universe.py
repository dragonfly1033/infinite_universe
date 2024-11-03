import pygame as pg

class Universe:
    def __init__(self, type, seed, W, H, callback):
        self.callback = callback
        self.type = type
        self.WIDTH = W
        self.HEIGHT = H
        self.seed = seed
        self.sector_size = 36
        self.cX = 0
        self.cY = 0
        self.vel = 4
        self.universeScreen = pg.Surface((self.WIDTH, self.HEIGHT))
        self.nSectorX = self.WIDTH//self.sector_size
        self.nSectorY = self.HEIGHT//self.sector_size
      

    def lehmer(self, low, high):
        self.seed += 0xe120fc15
        tmp = self.seed * 0x4a39b70d
        m1 = (tmp >> 32) ^ tmp
        tmp = m1 * 0x12fad5c9
        m2 = (tmp >> 32) ^ tmp
        return m2%(high-low) + low


    def setup(self):

        self.universeScreen.fill((0,0,0))
        for y in range(self.nSectorY):
            for x in range(self.nSectorX):
                sectorX = (self.cX//self.sector_size) + x
                sectorY = (self.cY//self.sector_size) + y 
                px = sectorX*self.sector_size - self.cX
                py = sectorY*self.sector_size - self.cY
                self.seed = sectorY << 16 | abs(sectorX+360)
                if self.lehmer(0,15) == 0:
                    colour = (self.lehmer(0,256), self.lehmer(0,256), self.lehmer(0,256))
                    r = self.lehmer(5,(self.sector_size-1)//2)
                    pg.draw.circle(self.universeScreen, colour, (px+(self.sector_size//2), py+(self.sector_size//2)), r)
                    
        

    def event_loop(self, event, dt):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(event.pos)
                cursor_x, cursor_y = event.pos
                sectorX = (self.cX + cursor_x)//self.sector_size
                sectorY = (self.cY + cursor_y)//self.sector_size
                self.seed = sectorY << 16 | abs(sectorX+360)
                if self.lehmer(0,15) == 0:
                    self.callback(2, self.seed)
                    
                    
    
    def game_loop(self):
        keys = pg.key.get_pressed()
        tempVel = self.vel

        if keys[pg.K_LSHIFT]:
            tempVel = self.vel*2
        elif keys[pg.K_LCTRL]:
            tempVel = self.vel//4
        else:
            tempVel = self.vel

        if keys[pg.K_w]:
            self.cY -= tempVel
            self.setup()
        if keys[pg.K_a]:
            self.cX -= tempVel
            self.setup()
        if keys[pg.K_s]:
            self.cY += tempVel
            self.setup()
        if keys[pg.K_d]:
            self.cX += tempVel
            self.setup()

    def get_surface(self) -> pg.Surface:
        return self.universeScreen





