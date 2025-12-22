import pygame
import random

class BSPNode:

    def __init__(self, space: pygame.Rect, left = None, right = None, room = None):
        self.space = space
        self.left = left
        self.right = right

    def split(self) -> None:
        direction = random.randint(0, 1)
        offset = random.uniform(0.2, 0.8)

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

def generate_dungeon(initial_space, room_ratio = 2.5):
    pass