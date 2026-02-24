from __future__ import annotations
import pygame
import random

class BSPNode:
    """
    Implements node for the binary space partitioning tree, used for generating video game maps

    Attributes:
        space (pygame.Rect): the total area that the node covers on the map
        left (BSPNode|None): a pointer to the left child node 
        right (BSPNode|None): a pointer to the right child node
    """

    def __init__(self, space: pygame.Rect, left: BSPNode|None = None, right: BSPNode|None = None, room = None):
        self.space = space
        self.left = left
        self.right = right

    def split(self, direction: int, offset: float) -> None:
        """
        Used to split node area (space attribute) into two sub-spaces to be stored in the left and right child nodes

        Args:
            direction (int): determines whether the area is split horizontally (1) or vertically (0)
            offset (float): a decimal value that decides where the split will be made. Ex) .60 -> one half will be 60% of the area and the other will be 40%
        """
        # Vertical split
        if direction == 0:
            left_area = self.space.scale_by(offset, 1)
            right_area = self.space.scale_by(1 - offset, 1)

            left_space = pygame.Rect((self.space.topleft), (left_area.size))
            right_space = pygame.Rect((left_space.topright[0], left_space.topright[1]), (right_area.size))
        # Horizontal split
        else:
            left_area = self.space.scale_by(1, offset)
            right_area = self.space.scale_by(1, 1 - offset)

            left_space = pygame.Rect((self.space.topleft), (left_area.size))
            right_space = pygame.Rect((left_space.bottomleft[0], left_space.bottomleft[1]), (right_area.size))

        # Initialize children
        self.left = BSPNode(left_space)
        self.right = BSPNode(right_space)

    def generate_room(self, min_area_coverage: float = .50):
        # How do I get a rectangle within a rectangle?
        # To ensure it isnt tiny I can compare the outer rect to the inner rect

        if self.right or self.left:
            return

        self.room = self.space.copy()

        # Scale down?
        scale_x = random.uniform(0.4, 0.9)
        scale_y = random.uniform(0.4, 0.9)
        self.room.scale_by_ip(scale_x, scale_y)

    

class BSPTree:
    """
    Used to generate the tree structure using BSP Nodes
    """

    @staticmethod
    def generate_tree(root: BSPNode, space_ratio: float = 1.75, min_size: int = 20, depth: int = 5) -> None:
        """
        Generates the tree recursively until the minimum size is exceeded or the target depth is reached

        Args:
            root (BSPNode): the root node of the tree
            space_ratio (float): the max x:y size ratio that the children node can be to avoid slender spaces
            min_size (int): the minimum size that a child node can be
            depth (int): the desired amount of depth for the tree
        """
        space = root.space

        if depth == 0:
            return
        
        # Stop if either dimension is too small
        if space.size[0] <= min_size or space.size[1] <= min_size:
            return
        
        # (REFACTOR LATER) Attempts to get a better split           
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

    def traverse(root: BSPNode) -> list[BSPNode]:
        """
        This traverses the tree

        Args:
            root (BSPNode): the root node of the tree to traverse
        
        Returns:
            (list[BSPNode]): List of all of the nodes in the tree
        """
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