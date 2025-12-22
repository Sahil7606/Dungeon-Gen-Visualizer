import sys, pygame
from bsp import BSPNode
pygame.init()

# Initializes screen
size =  width, height = 640, 480
screen = pygame.display.set_mode(size)
default_blue = (16, 38, 66)

space = pygame.Rect((width // 2) - 300, (height // 2) - 220, 600, 440)
bsp_node = BSPNode(space)
bsp_node.split()

# Runs until X button pressed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, default_blue, bsp_node.space, 10)
    pygame.draw.rect(screen, default_blue, bsp_node.left.space, 10)
    pygame.draw.rect(screen, default_blue, bsp_node.right.space, 10)
    pygame.display.flip()