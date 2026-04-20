from vec2 import vec2
from math import sqrt
import pygame

class Planet:
    def __init__(self, x, y, mass, vel = vec2(0,0)):
        self.pos = vec2(x, y)
        self.vel = vel
        self.mass = mass
        self.G = 100
        self.EPSILON = 5
        self.trail = []
        self.radius = 20
        self.maxTrailSize = 1000
        self.frameNumber = 0
    def update(self, window : pygame.Surface):
        pygame.draw.circle(window, (255,0,0), (self.pos.x, self.pos.y), self.radius)
        self.frameNumber+=1
        if self.frameNumber % 3 != 0:
            pass
        self.frameNumber = 0
        self.trail.append(self.pos)
        if len(self.trail) > self.maxTrailSize:
            self.trail.pop(0)
        last = -1
        for point in self.trail:
            if last==-1:
                last = point
                continue
            
            pygame.draw.line(window, (0,0,255), (last.x, last.y), (point.x, point.y))
            last = point
    def compare(self, other) -> vec2:
        delta = other.pos - self.pos                   
        r = delta.magnitude()
        f = self.G * self.mass * other.mass / (r**2 + self.EPSILON**2)
        return delta.normalized() * f 