import sys, pygame
from bsp import BSPNode, BSPTree
pygame.init()

# Initializes screen
size =  width, height = 1280, 720
screen = pygame.display.set_mode(size)
default_blue = (16, 38, 66)

space = pygame.Rect((width // 2) - 600, (height // 2) - 320, 1200, 640)
initial_area = BSPNode(space)
BSPTree.generate_tree(initial_area, 2, 150, 5)
spaces = BSPTree.traverse(initial_area)

for space in spaces:
    space.generate_room();

# Runs until X button pressed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
           
    screen.fill((255, 255, 255))

    

    for space in spaces:
        #pygame.draw.rect(screen, default_blue, space.space, 2)
        
        if not space.right and not space.left:
            pygame.draw.rect(screen, default_blue, space.room, 2)
        

    pygame.display.flip()