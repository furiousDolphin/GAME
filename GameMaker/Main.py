import pygame
from Scripts.Utils import load_image, load_images

from Programs.Menu import Menu
from Programs.AutotilePatterns import AutotilePatterns
from Programs.TileEdges import TileEdges
from Programs.LevelEditor import LevelEditor
from Programs.Game import Game



class Main():
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode((960, 540))
        self.clock = pygame.time.Clock()


        self.assets = {
            "Player": load_image("Player.png"),
            "Projectile": load_image("Projectile.png"),
            "Terrain": load_images("Terrain"),
            "Gun": load_image("Gun.png")
        }




        self.mode = "Menu"
        self.previous_mode = ""

    

        self.Menu = Menu(self, (960, 540))
        self.AutotilePatterns = AutotilePatterns(self, (960, 540))
        self.TileEdges = TileEdges(self, (960, 540))
        self.TileEdges.load("tile_edges.json")
        

        self.LevelEditor = LevelEditor(self, (960, 540))
        self.Game = Game(self, (960, 540))

        




    def run(self):
        while True:

            

            if self.previous_mode != self.mode:                
                self.previous_mode = self.mode

                if self.mode == "Menu":
                    self.screen = pygame.display.set_mode(self.Menu.screen_size)

                elif self.mode == "AutotilePatterns":
                    self.screen = pygame.display.set_mode(self.AutotilePatterns.screen_size)
                    
                elif self.mode == "LevelEditor":
                    self.screen = pygame.display.set_mode(self.LevelEditor.screen_size)

                elif self.mode == "Game":
                    self.screen = pygame.display.set_mode(self.Game.screen_size)
                    self.Game.tilemap.load('map.json')
                    self.Game.tile_edges = self.TileEdges.load('tile_edges.json')

                    self.Game.intersections.clear()
                    self.Game.centroid_vectors.clear()


            



            if self.mode == "Menu":
                self.Menu.run()

            elif self.mode == "AutotilePatterns":
                self.AutotilePatterns.run()

            elif self.mode == "TileEdges":
                self.TileEdges.run()
            
            elif self.mode == "LevelEditor":
                self.LevelEditor.run()

            elif self.mode == "Game":
                self.Game.run()



            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    main = Main()
    main.run()