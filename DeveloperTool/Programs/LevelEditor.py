import pygame
import sys
from Scripts.Tilemap import Tilemap
from Scripts.Buttons import Button2

RENDER_SCALE = 3

BUTTONS = {
            "Menu": Button2((100, 100), 24, "MENU").copy()
        }

class LevelEditor():
    def __init__(self, main, screen_size):

        self.main = main
        self.screen_size = screen_size
        self.surf = pygame.Surface((self.screen_size[0]//RENDER_SCALE, 
                                    self.screen_size[1]//RENDER_SCALE))

        self.tilemap = Tilemap(self.main, 16)

        self.surf_button = pygame.Surface((200, 200))
        self.surf_button.fill("#ff12f3")
        self.surf_button.set_colorkey("#ff12f3")


        self.movement = [False, False, False, False]
        self.offset = (0, 0)
        self.offgrid = False

        self.left_clicking = False
        self.right_clicking = False
        
        self.tile_variant = 0
        self.tile_category = 0 
        
    def movement_method(self):

        movement_frame = (self.movement[3] - self.movement[2], self.movement[1] - self.movement[0])
        self.offset = (self.offset[0] + movement_frame[0]*2, self.offset[1] + movement_frame[1]*2)
    
    def event_method(self):

        self.left_clicking = False
        self.right_clicking = False

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.left_clicking = True
                if event.button == 3:
                    self.right_clicking = True

                if event.button == 4:
                    self.tile_variant = (self.tile_variant + 1) % len(self.main.assets["Terrain"])
                if event.button == 5:
                    self.tile_variant = (self.tile_variant - 1) % len(self.main.assets["Terrain"])

                    


            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    self.left_clicking = False
                if event.button == 3:
                    self.right_clicking = False




            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                        self.movement[0] = True
                if event.key == pygame.K_s:
                    self.movement[1] = True
                if event.key == pygame.K_a:
                    self.movement[2] = True
                if event.key == pygame.K_d:
                    self.movement[3] = True

                if event.key == pygame.K_UP:
                    self.tile_variant = (self.tile_variant + 1) % len(self.main.assets["Terrain"])             
                if event.key == pygame.K_DOWN:
                    self.tile_variant = (self.tile_variant - 1) % len(self.main.assets["Terrain"])



                if event.key == pygame.K_g:
                    self.offgrid = not self.offgrid
                if event.key == pygame.K_o:
                    self.tilemap.save('map.json')



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.movement[0] = False
                if event.key == pygame.K_s:
                    self.movement[1] = False
                if event.key == pygame.K_a:
                    self.movement[2] = False
                if event.key == pygame.K_d:
                    self.movement[3] = False

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def button_method(self):
        mx, my = pygame.mouse.get_pos()

        for button_name in BUTTONS:
            button = BUTTONS[button_name]

                
            if button.update((mx, my)):

                if self.left_clicking:    
                                
                    if button_name == "Menu":
                            self.main.mode = "Menu" 
                            
            button.render(self.surf_button)

    def render_method(self):
        self.tilemap.render(self.surf, self.offset)
        self.main.screen.blit(pygame.transform.scale(self.surf, self.main.screen.get_size()), (0, 0))
        self.main.screen.blit(self.surf_button, (0, 0))
                
    def run(self):

        self.surf.fill("#9fa0ab")

        self.movement_method()
        self.button_method()



        mx, my = pygame.mouse.get_pos()
        pos = (int(mx / RENDER_SCALE + self.offset[0]), int(my / RENDER_SCALE + self.offset[1]))

        img = self.main.assets["Terrain"][self.tile_variant].copy()
        img.set_alpha(155)


        if not self.offgrid:
            pos = (pos[0]//self.tilemap.tile_size, pos[1]//self.tilemap.tile_size)
            self.surf.blit(img, (pos[0]*self.tilemap.tile_size - self.offset[0], pos[1]*self.tilemap.tile_size - self.offset[1]))

            if self.left_clicking:
                loc = str(pos[0]) + ";" + str(pos[1])
                if not loc in self.tilemap.tilemap:
                        self.tilemap.tilemap[loc] = {"variant": self.tile_variant, "pos": pos}

                
            if self.right_clicking:
                loc = str(pos[0]) + ";" + str(pos[1])
                if loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[loc]
                
        else:
            self.surf.blit(img, (pos[0]  - self.offset[0], pos[1]  - self.offset[1]))

            if self.left_clicking:
                self.tilemap.offgrid_tiles.append({"variant": self.tile_variant, "pos": pos})

            if self.right_clicking:
                pass



        self.event_method()
        self.render_method()