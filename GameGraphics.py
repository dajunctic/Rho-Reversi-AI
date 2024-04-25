import pygame

def drawRect(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def drawImage(surface, image, x = 0 , y = 0):
    surface.blit(image, (x, y))

class Image:
    def __init__(self, path):
        self.rect = pygame.Rect(0, 0 , 0 ,0)
        self.path = path
        self.image = self.load()
    def load(self):
        return pygame.image.load(self.path)
    def setRect(self, rectt):
        self.rect = rectt
    def setPos(self, x , y):
        self.rect.x = x
        self.rect.y = y
    def scale(self, sizeX, sizeY):
        self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
    def flip(self, boolX, boolY):
        self.image = pygame.transform.flip(self.image, boolX, boolY)
    def show(self, surface):
        drawImage(surface, self.image, self.rect.x, self.rect.y)

# Text #
DefaultFont = "data/font/rimouski.sb-regular.otf"
DefaultSize = 32
DefaultColor = pygame.Color(255 , 255 , 255)

class Text:
    
    def __init__(self) -> None:
        self.text = "Dajunctic rat dep trai"
        self.font = DefaultFont
        self.size = DefaultSize
        self.color = DefaultColor
        self.rect = pygame.Rect(0 , 0 , 0, 0)

    def setSize(self, size):
        self.size = size
        
    def setRect(self, object):
        self.rect.x = object.x
        self.rect.y = object.y
        self.rect.w = object.w
        self.rect.h = object.h
        
    def setPos(self, x , y):
        self.rect.x = x
        self.rect.y = y
        
    def setText(self, text):
        self.text = text
        
    def setFont(self, font):
        self.font = font
    
    def setColor(self, color):
        self.color = color

    def show(self, surface):
        LargeText = pygame.font.Font(self.font ,self.size)

        TextSurface = LargeText.render(self.text, True, self.color)
        TextRect = TextSurface.get_rect()

        TextRect.center = (self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2)
        surface.blit(TextSurface, TextRect)

class Animation(pygame.sprite.Sprite):
    def __init__(self, x , y, path, frame):
        super().__init__()
        self.sprite_count = frame
        self.current_sprite = 0

        self.sprites = []
        self.LoadSprites(path)
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def loadSprites(self, path):
        path = "Data/img/" + path
        for i in range(self.sprite_count):
            te = str(i + 1)
            for i in range(3 - len(te)):
                te = '0' + te
            self.sprites.append(pygame.image.load(path + te + ".png"))

    def update(self, speed):
        self.current_sprite += speed
        self.current_sprite %= self.sprite_count

        self.image = self.sprites[int(self.current_sprite)]
