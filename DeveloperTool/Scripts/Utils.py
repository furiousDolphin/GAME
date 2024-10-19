
import pygame
import math
import random
from sympy.solvers import solve
from sympy import Symbol, sin
import os

BASE_PATH = "C:/Users/topto/Desktop/uggy_toad/DeveloperTool/images/"

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
    for image_name in sorted(os.listdir(BASE_PATH + path)):
        images.append(load_image(path + "/" + image_name))
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

def linear_function(pixels = [[0, 0], [0, 0]], line_dx = 0, line_dy = 0, scale = 1):

    #pixels = [[int(pixels[0][0]//1), int(pixels[0][1]//1)], [int(pixels[1][0]//1), int(pixels[1][1]//1)]]
    
    if line_dx == 0:
        line_dx = abs(pixels[1][0] - pixels[0][0])
    if line_dy == 0:
        line_dy = abs(pixels[1][1] - pixels[0][1])

    line = []

    if line_dx < line_dy:
        if pixels[0][1] < pixels[1][1]:
            x1 = pixels[0][0]
            y1 = pixels[0][1]

            x2 = pixels[1][0]
            y2 = pixels[1][1]

        else:
            x1 = pixels[1][0]
            y1 = pixels[1][1]

            x2 = pixels[0][0]
            y2 = pixels[0][1]

        a = (x2 - x1) / (y2 - y1)
        
        for y in range(0, int(((y2 - y1)*scale + 1)//1)):
            x = a*y
            line.append([int((x + x1)//1), int((y + y1)//1)])
            

    else:
        if pixels[0][0] < pixels[1][0]:
            x1 = pixels[0][0]
            y1 = pixels[0][1]

            x2 = pixels[1][0]
            y2 = pixels[1][1]

        else:
            x1 = pixels[1][0]
            y1 = pixels[1][1]

            x2 = pixels[0][0]
            y2 = pixels[0][1]

        a = (y2 - y1) / (x2 - x1)
    
        for x in range(0, int(((x2 - x1)*scale + 1)//1)):
            y = a*x
            line.append([int((x + x1)//1), int((y + y1)//1)])
        
    return line

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

def function(pixels = [[0, 0], [0, 0]], outline = []):
    
    lines = []

    if pixels[0] != pixels[1]:        
        index_0 = outline.index(pixels[0])
        index_1 = outline.index(pixels[1])
        length = len(outline)
        clip = []
        
        if abs(index_1 - index_0) < length/2:

            if index_1 > index_0:
                clip = outline[index_0:index_1 + 1]
            else:
                clip = outline[index_1:index_0 + 1]
        else:
            if index_1 > index_0:
                clip = outline[index_1:] + outline[:index_0 + 1]
            else:
                clip = outline[index_0:] + outline[:index_1 + 1]

        for n in range(len(clip)):
            clip[n] = list(clip[n])

        clip_dx = abs(clip[-1][0] - clip[0][0])
        clip_dy = abs(clip[-1][1] - clip[0][1])

        line_dx = abs(pixels[1][0] - pixels[0][0])
        line_dy = abs(pixels[1][1] - pixels[0][1])  
     

        line = linear_function(pixels, line_dx, line_dy, 1)
        

        if len(line) == len(clip) and (line != clip or line != clip.reverse()):

            if line[0] != clip[0]:
                clip.reverse()
            
            
            highest_correctness = 0

            long_line = linear_function(pixels, line_dx, line_dy, 3)
            
            
            length = len(line)
            
            for n in range(len(long_line) - length +1):
                line.clear()

                for index in range(n, n + length):
                    line.append([long_line[index][0], long_line[index][1]])

                
                

                if line_dx == clip_dx and line_dy == clip_dy:
                    offset = (line[0][0] - clip[0][0], line[0][1] - clip[0][1])
                    correctness = 0
                    
                    

                    for n in range(length):
                        
                        
                        line[n][0] -= offset[0]
                        line[n][1] -= offset[1]
                        

                        if line[n] == clip[n]:
                            correctness += 1


                    if correctness == len(clip):
                        return [line]

                    elif correctness > highest_correctness and line not in lines:
                        
                        lines.clear()
                        lines.append([[line[index][0], line[index][1]] for index in range(length)])

                        highest_correctness = correctness

                    elif correctness == highest_correctness and line not in lines:
                        
                        lines.append([[line[index][0], line[index][1]] for index in range(length)])
            
                    
                        
            return lines               
            
        else:
            
            return [line]
   