import pygame
from GameDisplay import Display

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GAME_TITLE = "Rho Reversi"
GAME_ICON = "icon.png"

FPS = 60

black = (0,0,0)

class RhoPygame:
    def __init__(self) -> None:

        pygame.init()
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.icon = pygame.image.load(GAME_ICON)
        pygame.display.set_icon(self.icon)

        self.clock = pygame.time.Clock()
        self.running = True

        self.game = Display() 
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.surface.fill(black)
            self.game.show(self.surface)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                
            #    if e.type == pygame.KEYDOWN:
            #        self.game.keyDown(e.key);
                if e.type == pygame.KEYUP:
                    self.game.keyUp(e.key);
                    
                if self.game.menu.quit == True:
                    self.running = False;
                
                    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.game.keyPressed(pygame.K_LEFT)
            if keys[pygame.K_RIGHT]:
                self.game.keyPressed(pygame.K_RIGHT)
            if keys[pygame.K_DOWN]:
                self.game.keyPressed(pygame.K_DOWN)
            if keys[pygame.K_UP]:
                self.game.keyPressed(pygame.K_UP)

            pygame.display.update()
        
        pygame.quit()


if __name__ == "__main__":
    main = RhoPygame()
    main.run()
