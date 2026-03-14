from __future__ import annotations
import pygame
import random

# TODO: Find node neighbors
# TODO: Draw hallways
# TODO: Connect into one polygon

# NEXT: review and reorganize

class Rect:
    def __init__(self, top_left: tuple[int], width: int, height: int):
        self.top_left = top_left
        self.width = width
        self.height = height

    @property
    def bottom_right(self):
        return (self.top_left[0] + self.width, self.top_left[1] + self.height)
    
    @property
    def bottom_left(self):
        return (self.top_left[0], self.top_left[1] + self.height)
    
    @property
    def top_right(self):
        return (self.top_left[0] + self.width, self.top_left[1])

class BSPNode:
    """
    Implements node for the binary space partitioning tree, used for generating video game maps

    Attributes:
        space (Rect): the total area that the node covers on the map
        left (BSPNode|None): a pointer to the left child node 
        right (BSPNode|None): a pointer to the right child node
        room (Rect): the playable area within the space of the node
    """

    def __init__(self, space: Rect):
        self.space = space
        self.left = None
        self.right = None
        self.room = None

    def split(self, direction: int, offset: float) -> None:
        """
        Used to split node area (space attribute) into two sub-spaces to be stored in the left and right child nodes

        Args:
            direction (int): determines whether the area is split horizontally (1) or vertically (0)
            offset (float): a decimal value that decides where the split will be made. Ex) .60 -> one half will be 60% of the area and the other will be 40%
        """
        # Vertical split
        if direction == 0:
            left_space = Rect(self.space.top_left, int(self.space.width * offset), self.space.height)
            right_space = Rect(left_space.top_right, self.space.width - left_space.width, self.space.height)
        # Horizontal split 
        else:
            left_space = Rect(self.space.top_left, self.space.width, int(self.space.height * offset))
            right_space = Rect(left_space.bottom_left, self.space.width, self.space.height - left_space.height)

        # Initialize child nodes
        self.left = BSPNode(left_space)
        self.right = BSPNode(right_space)

    def write_to_grid(self, grid: list[list[int]]) -> None:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j == self.space.top_left[0] or j == self.space.top_left[0] + self.space.width - 1) and (self.space.top_left[1] <= i <= self.space.top_left[1] + self.space.height - 1):
                    grid[i][j] = 0

                if (i == self.space.top_left[1] or i == self.space.top_left[1] + self.space.height - 1) and (self.space.top_left[0] <= j <= self.space.top_left[0] + self.space.width - 1):
                    grid[i][j] = 0

    # # (Refactor Later) Not random enough
    # def generate_room(self, min_area_coverage: float = .50):
        
    #     if self.right or self.left:
    #         return

    #     self.room = self.space.copy()

    #     # Scale down?
    #     scale_x = random.uniform(0.4, 0.9)
    #     scale_y = random.uniform(0.4, 0.9)
    #     self.room.scale_by_ip(scale_x, scale_y)


class BSPTree:
    """
    Used to generate the tree structure using BSP Nodes
    """

    def __init__(self, root: BSPNode):
        self.root = root

    @staticmethod
    def generate_tree(root, space_ratio: float = 1.75, min_size: int = 20, depth: int = 5) -> None:
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
        if space.width <= min_size or space.height <= min_size:
            return
        
        # (REFACTOR LATER) Attempts to get a better split           
        for i in range(30):

            direction = random.choice([0, 1])
            offset = random.uniform(0.35, 0.65)
            root.split(direction, offset)

            left_space = root.left.space
            right_space = root.right.space

            l_ratio = max(left_space.width / left_space.height, left_space.height / left_space.width)
            r_ratio = max(right_space.width / right_space.height, right_space.height / right_space.width)

            if (l_ratio <= space_ratio and r_ratio <= space_ratio):
                break

        # Generate tree from left and right nodes
        BSPTree.generate_tree(root.left, space_ratio, min_size, depth - 1)
        BSPTree.generate_tree(root.right, space_ratio, min_size, depth - 1)

    def get_leaves(self) -> list[BSPNode]:
        """
        Gets leaf nodes of the tree

        Args:
            root (BSPNode): the root node of the tree to get leaves from
        
        Returns:
            (list[BSPNode]): List of all of the leaves in the tree
        """
        stack = [self.root]
        output = []

        while stack:
            node = stack.pop()
            
            if not node.left and not node.right:
                output.append(node)

            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return output
    
    def write_to_grid(self, grid: list[list[int]]):
        for leaf in self.get_leaves():
            leaf.write_to_grid(grid)
    
    def get_neighbors():
        pass