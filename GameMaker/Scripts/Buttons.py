import pygame
pygame.font.init()


class Button2():
    def __init__(self, pos, font_size, statement="", color = "#3489eb"):
        self.pos = pos
        self.font_size = font_size
        self.statement = statement
        self.collision = False
        

        font = pygame.font.Font("C:/Users/topto/Desktop/minecraft-font/MinecraftBold-nMK1.otf", font_size)

        self.txt = {
            "Off": font.render(statement, True, (255, 255, 255)),
            "On": font.render(statement, True, color)
            }
        
        self.txt_rect = self.txt["Off"].get_rect(center = pos)
 
    def copy(self):
        return Button2(self.pos, self.font_size, self.statement)
    
    def update(self, mouse_pos=(0, 0)):
        mx, my = mouse_pos
        
        self.collision = False

        if self.txt_rect.collidepoint((mx, my)):
            self.collision = True

        return self.collision

    def render(self, surf):

        if self.collision:
            surf.blit(self.txt["On"], self.txt_rect)
        else:
            surf.blit(self.txt["Off"], self.txt_rect)