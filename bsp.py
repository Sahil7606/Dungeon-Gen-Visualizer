from __future__ import annotations
import pygame
import random

# TODO: Find node neighbors
# TODO: Draw hallways
# TODO: Connect into one polygon
# TODO: Optimize write_to_grid function

# Maybe later add more customization to room generation


class Rect:
    """
    Represents a rectangular area on the map using a top-left coordinate, width, and height.

    Attributes:
        top_left (tuple[int]): the top-left coordinate of the rectangle as (x, y)
        width (int): the width of the rectangle
        height (int): the height of the rectangle
    """

    def __init__(self, top_left: tuple[int, int], width: int, height: int) -> None:
        """
        Initializes a rectangle.

        Args:
            top_left (tuple[int]): the top-left coordinate of the rectangle as (x, y)
            width (int): the width of the rectangle
            height (int): the height of the rectangle
        """
        self.top_left = top_left
        self.width = width
        self.height = height

    @property
    def bottom_right(self) -> tuple[int, int]:
        """
        Gets the bottom-right coordinate of the rectangle.

        Returns:
            (tuple[int]): the bottom-right coordinate as (x, y)
        """
        return (self.top_left[0] + self.width, self.top_left[1] + self.height)
    
    @property
    def bottom_left(self) -> tuple[int, int]:
        """
        Gets the bottom-left coordinate of the rectangle.

        Returns:
            (tuple[int]): the bottom-left coordinate as (x, y)
        """
        return (self.top_left[0], self.top_left[1] + self.height)
    
    @property
    def top_right(self) -> tuple[int, int]:
        """
        Gets the top-right coordinate of the rectangle.

        Returns:
            (tuple[int]): the top-right coordinate as (x, y)
        """
        return (self.top_left[0] + self.width, self.top_left[1])
    
    # Writes node to a 2D list of integers
    def write_to_grid(self, grid: list[list[int]], filled: bool = False, value: int = 0) -> None:
        """
        Writes the rectangle into a 2D integer grid.

        Args:
            grid (list[list[int]]): the map grid to write the node boundaries to
            filled (bool): if true it writes the whole area to the grid, if false it writes the perimeter
            value (int): the number value that each cell of the rect will have on the grid
        """
        if not filled:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if (j == self.top_left[0] or j == self.top_left[0] + self.width - 1) and (self.top_left[1] <= i <= self.top_left[1] + self.height - 1):
                        grid[i][j] = value
                    elif (i == self.top_left[1] or i == self.top_left[1] + self.height - 1) and (self.top_left[0] <= j <= self.top_left[0] + self.width - 1):
                        grid[i][j] = value
        else:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if (self.top_left[0] <= j <= self.top_left[0] + self.width - 1) and (self.top_left[1] <= i <= self.top_left[1] + self.height - 1):
                        grid[i][j] = value
                    elif (self.top_left[1] <= i <= self.top_left[1] + self.height - 1) and (self.top_left[0] <= j <= self.top_left[0] + self.width - 1):
                        grid[i][j] = value

    def contains_line(self, direction: chr, origin: int) -> bool:
        if (direction == 'x'):
            return (self.top_left[1] <= origin < self.bottom_left[1])
        else:
            return (self.top_left[0] <= origin < self.top_right[0])


class BSPNode:
    """
    Implements node for the binary space partitioning tree, used for generating video game maps

    Attributes:
        space (Rect): the total area that the node covers on the map
        left (BSPNode|None): a pointer to the left child node 
        right (BSPNode|None): a pointer to the right child node
        room (Rect): the playable area within the space of the node
    """

    def __init__(self, space: Rect) -> None:
        """
        Initializes a BSP node with a space and no children.

        Args:
            space (Rect): the total area that the node covers on the map
        """
        self.space = space
        self.left = None
        self.right = None
        self.room = None

        self.split_direction = None

    @property
    def is_leaf(self) -> bool:
        return not (self.left or self.right)
    
    def split(self, direction: chr, offset: float) -> None:
        """
        Used to split node area (space attribute) into two sub-spaces to be stored in the left and right child nodes

        Args:
            direction (int): determines whether the area is split horizontally (1) or vertically (0)
            offset (float): a decimal value that decides where the split will be made. Ex) .60 -> one half will be 60% of the area and the other will be 40%
        """
        # Vertical split
        if direction == 'y':
            left_space = Rect(self.space.top_left, int(self.space.width * offset), self.space.height)
            right_space = Rect(left_space.top_right, self.space.width - left_space.width, self.space.height)
        # Horizontal split 
        else:
            left_space = Rect(self.space.top_left, self.space.width, int(self.space.height * offset))
            right_space = Rect(left_space.bottom_left, self.space.width, self.space.height - left_space.height)

        # Initialize child nodes
        self.left = BSPNode(left_space)
        self.right = BSPNode(right_space)

        self.split_direction = direction
    
    def generate_room(self) -> None:
        """
        Generates a room for the current space.
        """
        space = self.space
        
        # At minimum it will be roughly a quarter of the original area
        room_width = random.randint(int(space.width / 2) + 1, space.width - 1)
        room_height = random.randint(int(space.height / 2) + 1, space.height - 1)

        top_left_x = random.randint(1, space.width - room_width) + space.top_left[0]
        top_left_y = random.randint(1, space.height - room_height) + space.top_left[1]

        self.room = Rect((top_left_x, top_left_y), room_width, room_height)

    def get_leaves_on_line(self, direction: chr, origin: int, use_full_area: bool = True) -> list[BSPNode]:
        if not self.space.contains_line(direction, origin):
            return []
        
        out = []
        
        if not use_full_area and self.is_leaf:
            space = self.room
        else:
            space = self.space

        if self.is_leaf and space.contains_line(direction, origin):
            return [self]

        if (self.left.space.contains_line(direction, origin)):
            out += self.left.get_leaves_on_line(direction, origin, use_full_area)
        if (self.right.space.contains_line(direction, origin)):
            out += self.right.get_leaves_on_line(direction, origin, use_full_area)

        return out

            
class BSPTree:
    """
    Used to generate the tree structure using BSP Nodes
    """

    def __init__(self, root: BSPNode) -> None:
        """
        Initializes a BSP tree with a root node.

        Args:
            root (BSPNode): the root node of the tree
        """
        self.root = root

    def generate_next_level(self, space_ratio: float = 1.75, min_size: tuple[int, int] = (20, 10)) -> None:
        """
        Generates one additional level by splitting eligible leaf nodes.

        Args:
            tree (BSPTree): the tree whose leaves will be split
            space_ratio (float): the max x:y size ratio allowed for children spaces
            min_size (tuple[int]): the minimum width and height required to split
        """
        leaves = self.get_leaves()

        for leaf in leaves:
            space = leaf.space

            if space.width <= min_size[0] or space.height <= min_size[1]:
                continue

            # (REFACTOR LATER) Attempts to get a better split           
            for i in range(30):

                direction = random.choice(['x', 'y'])
                offset = random.uniform(0.35, 0.65)
                leaf.split(direction, offset)

                leaf.split_direction = direction

                left_space = leaf.left.space
                right_space = leaf.right.space

                # Causes divide by zero error for small areas
                l_ratio = max(left_space.width / left_space.height, left_space.height / left_space.width)
                r_ratio = max(right_space.width / right_space.height, right_space.height / right_space.width)

                if (l_ratio <= space_ratio and r_ratio <= space_ratio):
                    break

        return

    def generate_tree(self, space_ratio: float = 1.75, min_size: tuple[int, int] = (20, 10), depth: int = 5) -> None:
        """
        Generates the tree recursively until the minimum size is exceeded or the target depth is reached

        Args:
            root (BSPNode): the root node of the tree
            space_ratio (float): the max x:y size ratio that the children node can be to avoid slender spaces
            min_size (int): the minimum size that a child node can be
            depth (int): the desired amount of depth for the tree
        """

        for _ in range(depth):
            self.generate_next_level(space_ratio, min_size)

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
            
            if node.is_leaf:
                output.append(node)

            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return output
    
    def write_to_grid(self, grid: list[list[int]]) -> None:
        """
        Writes all leaf node borders to a 2D integer grid.

        Args:
            grid (list[list[int]]): the map grid to write the tree boundaries to
        """
        for leaf in self.get_leaves():
            leaf.space.write_to_grid(grid, False)
    