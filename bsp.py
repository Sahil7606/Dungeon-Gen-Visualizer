import sys, pygame
pygame.init()

# Initializes screen
size =  width, height = 640, 480
screen = pygame.display.set_mode(size)

# Runs until X button pressed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (16, 38, 66), ((width // 2) - 300, (height // 2) - 220, 600, 440), 10)
    pygame.display.flip()
