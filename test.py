'''
This script trials a grid based approach to BSP generation for better scalability and practicality
'''

import random

world = [[0] * 320] * 180

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
            left_space = Rect(self.top_left, int(self.width * offset), self.height)
            right_space = Rect(self.top_right, self.width - left_space.width, self.height)
        else:
            left_space = Rect(self.top_left, self.width, int(self.height * offset))
            right_space = Rect(self.bottom_left, self.width, self.height - left_space.height)

        self.left = Rect(left_space)
        self.right = Rect(right_space)


    
    
    

    