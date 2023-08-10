import numpy as np
import pygame

class Board:
    def __init__(self, size: tuple[float, float], position: tuple[float, float]) -> None:
        self.size = size
        self.position = position
        self.array = np.full((size[0], size[1]), None)
        for i, j in np.ndindex(self.array.shape):
            self.array[i, j] = Bead((i + self.position[0], j + self.position[1]))
        self.array[:,size[1] - 1] = np.full(size[0], None)
    
    def toggle(self, x: int, y: int) -> None:
        for j in range(len(self.array[x])):
            self.array[x, j] = Bead((x, j + self.position[1]))
        self.array[x][y] = None

    def update(self, group) -> None:
        for i, j in np.ndindex(self.array.shape):
            if isinstance(self.array[i, j], Bead):
                group.add(self.array[i, j])
                if self.array[i, j].clicked:
                    self.toggle(i, j)
        for i, j in np.ndindex(self.array.shape):
            global hovering
            if isinstance(self.array[i, j], Bead):
                if self.array[i, j].hover:
                    hovering = True
             
class Bead(pygame.sprite.Sprite):
    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__()
        self.position = position
        self.surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image = self.surface
        self.rect = self.image.get_rect(center = self.abspos(self.position))
        pygame.draw.ellipse(self.surface, (0, 0, 0), (0,10,50,30))
        self.clicked = False
        self.hover = False

    def abspos(self, grid_position) -> tuple[float, float]:
        return (grid_position[0] * 80 + 100, 425 - grid_position[1] * 30)

    def update(self, event_list) -> None:
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.hover = True
                else:
                    self.hover = False
        self.image = self.surface
        self.rect = self.image.get_rect(center = self.abspos(self.position))
    
class Frame(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.surface = pygame.Surface((1000, 500), pygame.SRCALPHA)
        for i in range(10):
            pygame.draw.rect(self.surface, (101, 67, 33), (95 + 80 * i, 200 -20, 10, 240 +40))
        pygame.draw.rect(self.surface, (179, 119, 59), (45, 460, 830, 20))
        pygame.draw.rect(self.surface, (179, 119, 59), (45, 160, 830, 20))
        pygame.draw.rect(self.surface, (179, 119, 59), (45, 260, 830, 20))
        pygame.draw.rect(self.surface, (179, 119, 59), (30, 160, 20, 320))
        pygame.draw.rect(self.surface, (179, 119, 59), (870, 160, 20, 320))

bottom = Board((10, 5), (0, 0))
top = Board((10, 2), (0, 6))
allBeads = pygame.sprite.Group()

# main
pygame.init()
pygame.display.set_caption("Abacus")
screen = pygame.display.set_mode([925, 500])    
clock = pygame.time.Clock()
run = True
while run:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False

    allBeads.update(event_list)
    allBeads.empty()

    hovering = False
    bottom.update(allBeads)
    top.update(allBeads)
    if hovering: pygame.mouse.set_cursor(*pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
    else: pygame.mouse.set_cursor(*pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

    screen.fill((255, 255, 255))
    screen.blit(Frame().surface, (0, 0))
    allBeads.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()