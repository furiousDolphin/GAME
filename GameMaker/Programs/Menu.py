import pygame
import sys
from Scripts.Buttons import Button2


BUTTONS = {
            "LevelEditor": Button2((480, 230), 24, "LevelEditor").copy(),
            "TileEdges": Button2((480, 300), 24, "TileEdges").copy(),
            "AutotilePatterns": Button2((480, 370), 24, "AutotilePatterns").copy(),
            "Game": Button2((480, 170), 24, "Game").copy()
        }

class Menu():

    def __init__(self, main, screen_size):
        self.main = main
        self.screen_size = screen_size
        self.surf = pygame.Surface(self.screen_size)

        self.left_clicking = False

    def run(self):
        self.surf.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()




        
        for button_name in BUTTONS:
            button = BUTTONS[button_name]
           
            if button.update((mx, my)):

                if self.left_clicking:                        
                    if button_name == "AutotilePatterns":
                        self.main.mode = "AutotilePatterns"
                        
                    elif button_name == "LevelEditor":
                        self.main.mode = "LevelEditor"

                    elif button_name == "TileEdges":
                        self.main.mode = "TileEdges"

                    elif button_name == "Game":
                        self.main.mode = "Game"

                        
            button.render(self.surf)
          
        self.left_clicking = False




        self.main.screen.blit(self.surf, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_clicking = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()