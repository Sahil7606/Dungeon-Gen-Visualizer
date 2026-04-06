# import sys, pygame
from bsp import Rect, BSPNode, BSPTree
from world import World
# pygame.init()

# # Initializes screen
# size =  width, height = 1280, 720
# screen = pygame.display.set_mode(size)
# default_blue = (16, 38, 66)

world = World(64, 36)
initial_space = Rect((1, 1), 62, 34)
tree = BSPTree(BSPNode(initial_space))

tree.write_to_grid(world.grid)
print(world)

for _ in range(5):
    BSPTree.generate_next_level(tree, 2, (0, 0))
    tree.write_to_grid(world.grid)
    input()
    print(world)

world.clear_world()
input()

for leaf in tree.get_leaves():
    leaf.generate_room()
    leaf.room.write_to_grid(world.grid, True)

print(world)


# space = pygame.Rect((width // 2) - 600, (height // 2) - 320, 1200, 640)
# initial_area = BSPNode(space)
# BSPTree.generate_tree(initial_area, 2, 150, 90)
# spaces = BSPTree.get_leaves(initial_area)

# for space in spaces:
#     space.generate_room()

# # Runs until X button pressed
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
           
#     screen.fill((255, 255, 255))

    

#     for space in spaces:
#         pygame.draw.rect(screen, default_blue, space.space, 2)

#         pygame.draw.rect(screen, default_blue, space.room, 2)
        

#     pygame.display.flip()

