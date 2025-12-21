import sys, pygame
pygame.init()

# Initializes screen
size =  width, height = 640, 480
screen = pygame.display.set_mode(size)
default_blue = (16, 38, 66)

# Runs until X button pressed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, default_blue, ((width // 2) - 300, (height // 2) - 220, 600, 440), 10)
    pygame.display.flip()

class BSPNode:

    def __init__(space: pygame.Rect, left = None, right = None, room = None):
        this.space = space
        this.left = left
        this.right = right

class BSPGenerator:

    def generate_dungeon(width, height, room_ratio) -> list[pygame.Rect]:
        pass