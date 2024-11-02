import pygame as pg

pg.init()

font = pg.font.Font(None, 36)
clock = pg.time.Clock()
display = pg.display.set_mode((1920, 1080))

class System:
    def __init__(self, name, color, x, y, radius, screen):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen

    def plot(self):
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

class Universe:
    def __init__(self, type, seed):
        self.type = type
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.seed = seed
        self.sector_size = 36
        self.cX = 0
        self.cY = 0
        self.vel = 4
        self.universeScreen = pg.Surface((self.WIDTH, self.HEIGHT))
        
        

    def lehmer(self, low, high):
        self.seed += 0xe120fc15
        tmp = self.seed * 0x4a39b70d
        m1 = (tmp >> 32) ^ tmp
        tmp = m1 * 0x12fad5c9
        m2 = (tmp >> 32) ^ tmp
        return m2%(high-low) + low



    def universeScreenSetup(self):
        nSectorX = self.WIDTH//self.sector_size
        nSectorY = self.HEIGHT//self.sector_size
        self.universeScreen.fill((0,0,0))
        for y in range(nSectorY):
            for x in range(nSectorX):
                sectorX = (self.cX//self.sector_size) + x
                sectorY = (self.cY//self.sector_size) + y 
                px = sectorX*self.sector_size - self.cX
                py = sectorY*self.sector_size - self.cY
                self.seed = sectorY << 32 | abs(sectorX+360)
                if self.lehmer(0,15) == 0:
                    colour = (self.lehmer(0,256), self.lehmer(0,256), self.lehmer(0,256))
                    r = self.lehmer(5,(self.sector_size-1)//2)
                    new = System(colour, px+(self.sector_size//2), py+(self.sector_size//2), r, self.universeScreen)
                    new.plot()
        coord = font.render(f'({self.cX},{self.cY})', False, (255,255,255))
        self.universeScreen.blit(coord, (0,0))

        

    def event_loop(self, event, dt):
        if event.type == pg.KEYDOWN:
            # if event.key == pg.K_a
            pass
    
    def game_loop(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            tempVel = self.vel*2
        elif keys[pg.K_LCTRL]:
            tempVel = self.vel//4
        if keys[pg.K_w]:
            self.cY -= tempVel
            self.universeScreenSetup()
        if keys[pg.K_a]:
            self.cX -= tempVel
            self.universeScreenSetup()
        if keys[pg.K_s]:
            self.cY += tempVel
            self.universeScreenSetup()
        if keys[pg.K_d]:
            self.cX += tempVel
            self.universeScreenSetup()

        pg.quit()
        quit()

    def get_surface(self) -> pg.Surface:
        pass





