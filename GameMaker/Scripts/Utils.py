
import pygame
import math
import random
from sympy.solvers import solve
from sympy import Symbol, sin
import os

BASE_PATH = "images/"

#C:/Users/topto/Desktop/

def combinations(elements):
    if len(elements) == 0:
        return [[]]
    
    first_element = elements[0]
    rest = elements[1:]

    combs_without_first = combinations(rest)
    combs_with_first = [comb + [first_element] for comb in combs_without_first.copy()]

    return combs_with_first + combs_without_first


def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def get_angle(start = (0, 0), stop = (0, 0)):

    x, y = stop
         
    r = math.sqrt((x - start[0])**2 + (y - start[1])**2)

    SIN = (y - start[1])/r
    COS = (x - start[0])/r

    a = Symbol('a')
    angle = solve(sin(a) - SIN, a)
    if x - start[0] > 0: angle = float(angle[1])/math.pi*180 + 180
    else: angle = float(angle[0])/math.pi*180 + 180

    return angle  #if x - start[0] > 0: float(angle[1])/math.pi*180+180 else float(angle[0])/math.pi*180+180


def reflection(vector_ab = (0, 0), vector_1 = (0, 0)):

    vector_2 = [0, 0]
    a, b = vector_ab
    x, y = vector_1

    vector_2[0] = (2*a*b) / (b**2 + a**2) * y - (b**2 - a**2) / (b**2 + a**2) * x
    vector_2[1] = (2*a*b) / (b**2 + a**2) * x + (b**2 - a**2) / (b**2 + a**2) * y

    return vector_2

def spark_datas(vector_ab = (0, 0), vector_2 = (0, 0)):
    a, b = vector_ab
    x, y = vector_2

    COS = (a*x + b*y)/math.sqrt((a**2 + b**2)*(x**2 + y**2))
    SIN = random.uniform(0, math.sqrt(1-COS**2)*0.8)

    COS = math.sqrt(1-SIN**2)
    
    vector_3 = [0, 0]

    vector_3[1] = random.choice((
        (COS*y + math.sqrt(x**2*(1 - COS**2))),
        (COS*y - math.sqrt(x**2*(1 - COS**2)))
    ))

    vector_3[0] = ((x**2 + y**2)*COS - y*vector_3[1])/(x+0.01)

    return [vector_3, COS]


   