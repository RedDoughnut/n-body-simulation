import math
import pygame
class vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return vec2(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        mag = self.magnitude()
        if mag == 0:
            return vec2(0, 0)
        return vec2(self.x / mag, self.y / mag)

    def direction(self):
        return math.atan2(self.y, self.x) 

    def __repr__(self):
        return f"Vector2({self.x:.2f}, {self.y:.2f})"