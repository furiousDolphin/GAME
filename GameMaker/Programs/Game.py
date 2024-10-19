import pygame
import sys
from Scripts.Utils import get_angle, reflection, spark_datas
from Scripts.Tilemap import Tilemap
from Scripts.Entities import Entity
from Scripts.Projectile import Projectile
from Scripts.Spark import Spark
from Scripts.Buttons import Button2


RENDER_SCALE = 3

BUTTONS = {
            "Menu": Button2((100, 100), 24, "MENU").copy()
        }

class Game():
    def __init__(self, main, screen_size):

        
        self.main = main
        self.screen_size = screen_size       
        self.surf = pygame.Surface((self.screen_size[0]//RENDER_SCALE, self.screen_size[1]//RENDER_SCALE))

        self.surf_button = pygame.Surface((200, 200))
        self.surf_button.fill("#ff12f3")
        self.surf_button.set_colorkey("#ff12f3")

        self.left_clicking = False
        self.frame = 0


        self.movement = [False, False, False, False]
        self.render_scroll = [0, 0]


        self.tilemap = Tilemap(self.main, 16)
        self.tile_edges = {}


        self.player = Entity(self.main, "Player", (24, 24), (100, 100))


        
        self.gun_img = self.main.assets["Gun"]
        self.projectile_img = self.main.assets["Projectile"]

        self.projectiles = []
        self.intersections = []
        self.sparks = []



        self.centroid_vectors = []  #PRZYDATNE

    def button_method(self):
        mx, my = pygame.mouse.get_pos()

        for button_name in BUTTONS:
            button = BUTTONS[button_name]

                
            if button.update((mx, my)):

                if self.left_clicking:    
                                
                    if button_name == "Menu":
                            self.main.mode = "Menu" 
                            
            button.render(self.surf_button)

    def projectiles_method(self):

        if self.projectiles:
            for projectile in self.projectiles.copy():

                if projectile.update():

                    self.intersections.append(projectile.intersection.copy())



                    edge = projectile.edge.copy()
                    edge_vector = [edge[1][0] - edge[0][0], 
                                   edge[1][1] - edge[0][1]]
                    
                    reflected_movement = reflection(edge_vector, projectile.movement.copy())
                       
                    self.projectiles.remove(projectile)



                    for _ in range(6):
                        spark_movement, COS = spark_datas(edge_vector, reflected_movement)

                        self.sparks.append(Spark(self.intersections[-1], spark_movement, 1.5, 30, COS))
                                                
                else:
                    projectile.render(self.surf, self.offset)

    def sparks_method(self):

        if self.sparks:
            for spark in self.sparks.copy():

                if spark.update():
                    self.sparks.remove(spark)
                else:
                    spark.render(self.surf, self.offset)

    def render_method(self):

        self.player.update(self.tilemap, self.movement)
        self.player.render(self.surf, self.offset)
        self.tilemap.render(self.surf, self.offset)

        self.projectiles_method()
        self.sparks_method()

        mx, my = pygame.mouse.get_pos()

        pygame.draw.line(self.surf, (0, 0, 0), (self.player.pos[0] - self.offset[0] + 12,
                                                self.player.pos[1] - self.offset[1] + 12),
                                                (mx//RENDER_SCALE, my//RENDER_SCALE))
        

        if self.intersections:
            for intersection in self.intersections:
                pygame.draw.circle(self.surf, (0, 0, 0), (intersection[0] - self.offset[0],
                                                           intersection[1] - self.offset[1]), 1, 1)
                

        self.surf.blit(self.gun_img, (self.player.pos[0] - self.offset[0] + 12 - self.gun_img.get_width()/2,
                                       self.player.pos[1] - self.offset[1] + 12 - self.gun_img.get_height()/2))
        

        self.main.screen.blit(pygame.transform.scale(self.surf, self.screen_size), (0, 0))
        self.main.screen.blit(self.surf_button, (0, 0))

    def create_projectile(self):
        mx, my = pygame.mouse.get_pos()

        projectile_movement = pygame.math.Vector2((mx//RENDER_SCALE - (self.player.pos[0] - self.offset[0] + 12),
                                                   my//RENDER_SCALE - (self.player.pos[1] - self.offset[1] + 12)))

        projectile_pos = (self.player.pos[0] + 12 - self.projectile_img.get_width()/2,
                          self.player.pos[1] + 12 - self.projectile_img.get_height()/2)
                    
        projectile_movement.scale_to_length(3)

        self.projectiles.append(Projectile(self.main, self.projectile_img, self.tilemap, self.tile_edges, 
                                          (7, 7), projectile_pos, [projectile_movement[0], projectile_movement[1]]))
    
    def event_method(self):

        self.left_clicking = False

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.movement[0] = True
                if event.key == pygame.K_s:
                    self.movement[1] = True
                if event.key == pygame.K_a:
                    self.movement[2] = True
                if event.key == pygame.K_d:
                    self.movement[3] = True

                if event.key == pygame.K_SPACE:
                    self.create_projectile()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.movement[0] = False
                if event.key == pygame.K_s:
                    self.movement[1] = False
                if event.key == pygame.K_a:
                    self.movement[2] = False
                if event.key == pygame.K_d:
                    self.movement[3] = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.left_clicking = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):                    
        pygame.display.set_caption(f"{self.main.clock.get_fps()}")
        self.surf.fill("#9fa0ab")
            

        self.render_scroll[0] += (self.player.rect().centerx - self.surf.get_width()/2 - self.render_scroll[0]) / 30
        self.render_scroll[1] += (self.player.rect().centery - self.surf.get_height()/2 - self.render_scroll[1]) / 30
        self.offset = (int(self.render_scroll[0]), int(self.render_scroll[1]))

        mx, my = pygame.mouse.get_pos()

        if self.frame == 0:
            angle = get_angle((self.player.pos[0] - self.offset[0] + 12,
                               self.player.pos[1] - self.offset[1] + 12),
                               (mx//RENDER_SCALE, my//RENDER_SCALE))
            
            self.gun_img = pygame.transform.rotate(self.main.assets["Gun"], angle)

        self.frame = (self.frame + 1)%5


        self.button_method()
        self.event_method()
        self.render_method()