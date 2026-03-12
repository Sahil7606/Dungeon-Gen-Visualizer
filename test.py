'''
This script trials a grid based approach to BSP generation for better scalability and practicality
'''

import random

world = [[1] * 40 for _ in range(30)]

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
    def __init__(self, space: Rect):
        self.space = space
        self.left = None
        self.right = None

    def split(self):
        direction = random.choice([0, 1])
        offset =  random.uniform(0.35, 0.65)

        if direction == 0:
            left_space = Rect(self.space.top_left, int(self.space.width * offset), self.space.height)
            right_space = Rect(left_space.top_right, self.space.width - left_space.width, self.space.height)
        else:
            left_space = Rect(self.space.top_left, self.space.width, int(self.space.height * offset))
            right_space = Rect(left_space.bottom_left, self.space.width, self.space.height - left_space.height)

        self.left = BSPNode(left_space)
        self.right = BSPNode(right_space)

root = BSPNode(Rect((1, 1), 38, 28))

def write_to_grid(r: Rect):
    for i in range(len(world)):
        for j in range(len(world[i])):
            if (j == r.top_left[0] or j == r.top_left[0] + r.width - 1) and (r.top_left[1] <= i <= r.top_left[1] + r.height - 1):
                world[i][j] = 0

            if (i == r.top_left[1] or i == r.top_left[1] + r.height - 1) and (r.top_left[0] <= j <= r.top_left[0] + r.width - 1):
                world[i][j] = 0

root.split()
write_to_grid(root.left.space)
write_to_grid(root.right.space)

for row in world:
    string = ""
    for cell in row:
        string += (str(cell) + " ")

    print(string)
        


    
    
    

    