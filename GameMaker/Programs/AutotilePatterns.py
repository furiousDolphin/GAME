import pygame
import sys
from Scripts.Utils import combinations
from Scripts.Buttons import Button2





MATRIX = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

BUTTONS = {
            "next": Button2((860, 270), 24, "NEXT").copy(),
            "back": Button2((100, 270), 24, "BACK").copy(),
            "Menu": Button2((480, 270), 24, "MENU").copy()
        }

class AutotilePatterns():

    def __init__(self, main, screen_size):
        self.main = main
        self.screen_size = screen_size
        self.surf = pygame.Surface(self.screen_size)  #w grze będę to musiał podzielić przez SCALE
        self.surf.fill((0, 0, 0))
        
        self.left_clicking = False



        self.combinations = combinations(MATRIX)
        self.combinations.sort(key = lambda x: len(x))

        '''self.combination_dictionary = {}

        for n in range(len(self.combinations) + 1):
            self.combination_dictionary.update({str(n):[]})

        for combination in self.combinations:
            key = str(len(combination))
            if key in self.combination_dictionary:
                self.combination_dictionary[key].append(combination)
        '''


        self.page = 0
        self.max_page = len(self.combinations)
        
        self.pixels = self.combinations[0]




        self.img = pygame.Surface((3, 3))
        self.img.fill((255, 255, 255))



        self.SCALE = int(min(self.surf.get_height() / self.img.get_width(), self.surf.get_height() / self.img.get_height()))

        self.img = pygame.transform.scale(self.img, (self.img.get_width()*self.SCALE, self.img.get_height()*self.SCALE))
        self.img_shift = ((self.surf.get_width() - self.img.get_width())/2, (self.surf.get_height() - self.img.get_height())/2)



        self.blue_mark = pygame.Surface((self.SCALE, self.SCALE))
        self.blue_mark.fill("#3489eb")
        self.blue_mark.set_alpha(155)

        self.red_mark = pygame.Surface((self.SCALE, self.SCALE))
        self.red_mark.fill("#ff0000")
        self.red_mark.set_alpha(155)

    def run(self):


        self.surf.blit(self.img, self.img_shift)

        mx, my = pygame.mouse.get_pos()




        if self.pixels:
            for pos in self.pixels.copy():
                self.surf.blit(self.blue_mark, ((pos[0] + 1)*self.SCALE + self.img_shift[0], (pos[1] + 1)*self.SCALE + self.img_shift[1]))
        
        self.surf.blit(self.red_mark, (self.SCALE + self.img_shift[0], self.SCALE + self.img_shift[1]))




        
        for button_name in BUTTONS:
            button = BUTTONS[button_name]

            if not (button_name == "next" and self.page == self.max_page) and not (button_name == "back" and self.page == 0):
                if button.update((mx, my)):

                    if self.left_clicking:    
                                                                    
                        if button_name == "next":
                            self.page = min(self.page + 1, self.max_page)
                            self.pixels =  self.combinations[self.page]

                        if button_name == "back":
                            self.page = max(0, self.page - 1)
                            self.pixels =  self.combinations[self.page]

                        if button_name == "Menu":
                            self.main.mode = "Menu" 
                        
                button.render(self.surf)




        self.main.screen.blit(self.surf, (0, 0))




        self.left_clicking = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_clicking = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
