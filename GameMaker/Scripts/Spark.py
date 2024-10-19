import pygame
import random

class Spark():
    def __init__(self, pos, movement, q, d, COS=1):
        self.pos = list(pos)
        rand = max(0.4, random.random())
        self.movement = [rand*movement[0]*COS**2, rand*movement[1]*COS**2]
        self.frame = 0
        self.time = d
        self.done = False

        #d = x2 - x1 gdzie x1 = 0 a x2 to koniec przedziału 
        #q to maksimum funkcji kwadratowej z ujemnym a (gdy q jest dodatnie)

        self.a = -(4*q)/d**2
        self.b = (4*q)/d
        # c jest równe zero
    
        vector = pygame.math.Vector2((movement[0], movement[1]))
        vector.scale_to_length(2)
        vector = vector*COS**3


        self.points = [
            (-vector[0], -vector[1]),
            (vector[1]*0.3, -vector[0]*0.3),
            (vector[0], vector[1]),            
            (-vector[1]*0.3, vector[0]*0.3)
            
        ]
        
    def update(self):
        
        self.frame += 1
        
        self.size = (self.a*self.frame**2 + self.b*self.frame)**2  #funkcja kwadratowa podniesiona do kwadratu

        self.pos[0] += self.movement[0]
        self.pos[1] += self.movement[1]

        if self.frame > self.time:
            self.done = True

        return self.done

    def render(self, surf, offset=(0, 0)):
        pygame.draw.polygon(surf, (0, 0, 0), [[self.pos[0] + x*self.size - offset[0],
                                               self.pos[1] + y*self.size - offset[1]]
                                               for x, y in self.points])