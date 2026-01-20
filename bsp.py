import pygame
import random

class BSPNode:

    def __init__(self, space: pygame.Rect, left = None, right = None, room = None):
        self.space = space
        self.left = left
        self.right = right

    def split(self, direction, offset) -> None:

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

    def generate_room():
        pass

    

class BSPTree:

    @staticmethod
    def generate_tree(root, space_ratio = 1.75, min_size = 20, depth = 5):

        space = root.space

        if depth == 0:
            return
        
        # Stop if either dimension is too small
        if space.size[0] <= min_size or space.size[1] <= min_size:
            return
        
        # Attempts to get a better split
        for i in range(30):

            direction = random.choice([0, 1])
            offset =  random.uniform(0.35, 0.65)
            root.split(direction, offset)

            left_size = root.left.space.size
            right_size = root.right.space.size

            l_ratio = max(left_size[0] / left_size[1], left_size[1] / left_size[0])
            r_ratio = max(right_size[0] / right_size[1], right_size[1] / right_size[0])


            if (l_ratio <= space_ratio and r_ratio <= space_ratio):
                break

        BSPTree.generate_tree(root.left, space_ratio, min_size, depth - 1)
        BSPTree.generate_tree(root.right, space_ratio, min_size, depth - 1)

    def traverse(root):
        stack = [root]
        output = []

        while stack:
            node = stack.pop()
            output.append(node)

            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return output