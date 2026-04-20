from vec2 import vec2
from math import sqrt
import pygame

class Planet:
    def __init__(self, x, y, mass, vel = vec2(0,0)):
        self.pos = vec2(x, y)
        self.vel = vel
        self.mass = mass
        self.G = 1000
        self.EPSILON = 5
        self.trail = []
        self.maxTrailSize = 1000
        self.frameNumber = 0
    def update(self, window : pygame.Surface):
        pygame.draw.circle(window, (255,0,0), (self.pos.x, self.pos.y), 20)
        self.frameNumber+=1
        if self.frameNumber % 3 != 0:
            pass
        self.frameNumber = 0
        self.trail.append(self.pos)
        if len(self.trail) > self.maxTrailSize:
            self.trail.pop(0)
        for point in self.trail:
            pygame.draw.circle(window, (255,0,0), (point.x, point.y), 2)
    def compare(self, other) -> vec2:
        delta = other.pos - self.pos                   
        r = delta.magnitude()
        f = self.G * self.mass * other.mass / (r**2 + self.EPSILON**2)
        return delta.normalized() * f 