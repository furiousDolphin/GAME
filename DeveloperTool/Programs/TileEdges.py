import pygame
import sys
import json
from Scripts.Buttons import Button2


BUTTONS = {
            "next": Button2((860, 270), 24, "NEXT").copy(),
            "back": Button2((100, 270), 24, "BACK").copy(),
            "Menu": Button2((480, 270), 24, "MENU").copy()
        }

class TileEdges():
    def __init__(self, main, screen_size):
        self.main = main
        self.screen_size = screen_size
        self.surf = pygame.Surface(self.screen_size)

        self.change_img = True
        self.img_index = 0
        self.max_img_index = len(self.main.assets["Terrain"]) - 1


        self.left_clicking = False

        self.dictionary = {}

    def button_method(self):

        mx, my = pygame.mouse.get_pos()

        for button_name in BUTTONS:
            button = BUTTONS[button_name]


            if not (button_name == "next" and self.img_index == self.max_img_index) and not (button_name == "back" and self.img_index == 0):
                if button.update((mx, my)):


                    if self.left_clicking:                                               
                        
                        if button_name == "next":

                            self.dictionary[str(self.img_index)] = tuple(self.pixels)
                            self.pixels.clear()

                            self.img_index = min(self.img_index + 1, self.max_img_index)
                            self.change_img = True
                            


                        if button_name == "back":

                            self.dictionary[str(self.img_index)] = tuple(self.pixels)
                            self.pixels.clear()

                            self.img_index = max(0, self.img_index - 1)
                            self.change_img = True

                            

                        if button_name == "Menu":
                            self.main.mode = "Menu" 
                        
                button.render(self.surf)

    def event_method(self):


        self.left_clicking = False

        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    self.left_clicking = True                   

                    if self.pos not in self.pixels and self.pos in self.outline:
                        self.pixels.append(self.pos)


                if event.button == 3:
                    while self.pos in self.pixels:
                        self.pixels.remove(self.pos)
                        

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_o:
                    self.save("tile_edges.json")
                    #self.tilemap.save('map.json')



            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def save(self, path):
        self.dictionary[str(self.img_index)] = tuple(self.pixels)

        f = open(path, 'w')
        json.dump(self.dictionary, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        self.dictionary = json.load(f)
        f.close()
        
        return self.dictionary

    def run(self):

        if self.change_img:
            
            self.pixels = []
            self.change_img = False
            


            self.img = self.main.assets["Terrain"][self.img_index]
            self.img_mask = pygame.mask.from_surface(self.img)

            self.outline = [tuple(pos) for pos in self.img_mask.outline()][:-1]

            self.check_pos_surface = pygame.Surface((1, 1))
            self.check_pos_mask = pygame.mask.from_surface(self.check_pos_surface)



            self.SCALE = int(min(self.surf.get_height() / self.img.get_width(), self.surf.get_height() / self.img.get_height()))  # WAŻNA ZMIANA z width na height
            self.img = pygame.transform.scale(self.img, (self.img.get_width()*self.SCALE, self.img.get_height()*self.SCALE))
            self.img_shift = ((self.surf.get_width() - self.img.get_width())/2, (self.surf.get_height() - self.img.get_height())/2)
            self.img_rect = pygame.Rect(self.img_shift, self.img.get_size())



            self.cursor = pygame.Surface((self.SCALE, self.SCALE))
            self.white_mark = pygame.Surface((self.SCALE, self.SCALE))


            

            self.cursor.fill((255, 255, 255))
            self.cursor.set_alpha(100)

            self.white_mark.fill((255, 255, 255))
            self.white_mark.set_alpha(155)
                       

        self.surf.fill((0, 0, 0))
        self.surf.blit(self.img, self.img_shift)


        if self.pixels:
            for pos in self.pixels:
                self.surf.blit(self.white_mark, (pos[0]*self.SCALE + self.img_shift[0], pos[1]*self.SCALE + self.img_shift[1]))
                    
                    



        mx, my = pygame.mouse.get_pos()

        self.pos = (int((mx - self.img_shift[0])//self.SCALE), int((my - self.img_shift[1])//self.SCALE))

        if self.img_rect.collidepoint((mx, my)):
            if self.check_pos_mask.overlap(self.img_mask, (-self.pos[0], -self.pos[1])):

                self.surf.blit(self.cursor, (self.pos[0]*self.SCALE + self.img_shift[0],
                                             self.pos[1]*self.SCALE + self.img_shift[1]))
            


        self.button_method()
        self.event_method()     


        self.main.screen.blit(self.surf, (0, 0))