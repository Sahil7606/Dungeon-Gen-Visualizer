import pygame
import random

class BSPNode:

    def __init__(self, space: pygame.Rect, left = None, right = None, room = None):
        self.space = space
        self.left = left
        self.right = right

    def split(self) -> None:
        direction = random.randint(0, 1)
        offset = random.uniform(0.35, 0.65)

        if direction == 0:
            left_area = self.space.scale_by(offset, 1)
            right_area = self.space.scale_by(1 - offset, 1)

            left_space = pygame.Rect((self.space.topleft), (left_area.size))
            right_space = pygame.Rect((left_space.topright[0], left_space.topright[1]), (right_area.size))
        else:
            left_area = self.space.scale_by(1, offset)
            right_area = self.space.scale_by(1, 1 - offset)

            left_space = pygame.Rect((self.space.topleft), (left_area.size))
            right_space = pygame.Rect((left_space.bottomleft[0], left_space.bottomleft[1]), (right_area.size))

        self.left = BSPNode(left_space)
        self.right = BSPNode(right_space)

    def traverse(self):
        stack = [self]
        output = []

        while stack:
            node = stack.pop()
            output.append(node)

            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return output

def generate_dungeon(initial_area, room_ratio = 1.75, min_size = 20):
    space = initial_area.space
    
    # Prevent division by zero - stop if either dimension is too small
    if space.size[0] <= min_size or space.size[1] <= min_size:
        return
    
    # Add max iterations to prevent infinite loop
    MAX_ATTEMPTS = 100
    attempts = 0
    
    while True:
        initial_area.split()
        left_size = initial_area.left.space.size
        right_size = initial_area.right.space.size
        l_ratio = max(left_size[0] / left_size[1], left_size[1] / left_size[0])
        r_ratio = max(right_size[0] / right_size[1], right_size[1] / right_size[0])
        attempts += 1

        if (l_ratio >= room_ratio or r_ratio >= room_ratio) and attempts < MAX_ATTEMPTS:
            break

    generate_dungeon(initial_area.left, room_ratio, min_size)
    generate_dungeon(initial_area.right, room_ratio, min_size)