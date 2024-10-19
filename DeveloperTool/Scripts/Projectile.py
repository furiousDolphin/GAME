
import pygame
from Scripts.Utils import linear_function


class Projectile():
    def __init__(self, main, img, tilemap, tile_edges, size = (0, 0), pos=[0, 0], movement=(0, 0)):
        self.main = main
        #self.img = pygame.transform.rotate(img, angle)
        self.img = img
        self.tilemap = tilemap
        self.tile_edges = tile_edges
        self.size = size
        self.pos = list(pos)
        self.movement = movement
        self.tile_size = 16
        self.intersection = [0, 0]
        self.edge_vector = [0, 0]
        self.centroid = [0, 0]
        self.NEIGHBOR_OFFSETS = []
        
        for x in range(-1, int(size[0]//self.tile_size + 2)):
            for y in range(-1, int(size[1]//self.tile_size + 2)):
                self.NEIGHBOR_OFFSETS.append((x, y))
        
    def update(self):
        
        self.pos[0] += self.movement[0]
        self.pos[1] += self.movement[1]
        

        rect = pygame.Rect(self.pos, self.size)

        


        for tile in self.tilemap.tiles_around(self.pos, self.NEIGHBOR_OFFSETS):
            
            tile_rect = pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size,
                                    self.tile_size, self.tile_size)
            


            


            if rect.colliderect(tile_rect):

                img_mask = pygame.mask.from_surface(self.img)
                tile_mask = pygame.mask.from_surface(self.main.assets["Terrain"][tile["variant"]])   
                overlap_mask = tile_mask.overlap_mask(img_mask, (self.pos[0] - tile["pos"][0]*self.tile_size,
                                                                 self.pos[1] - tile["pos"][1]*self.tile_size))




                if overlap_mask:

                    overlap_centroid = overlap_mask.centroid()
                    if overlap_centroid == (0, 0):
                        overlap_centroid = tile_rect.topleft

                    x1, y1 = (overlap_centroid[0], overlap_centroid[1])
                    x2, y2 = (x1 - self.movement[0], y1 - self.movement[1])



                    pixels = self.tile_edges[str(tile["variant"])]
                    

                    for i in range(len(pixels) - 1):

                        x3, y3 = pixels[i]
                        x4, y4 = pixels[i + 1]



                        d = (y4 - y3)*(x2 - x1) - (y2 - y1)*(x4 - x3)

                        if d != 0:
                            t = ((y4 - y3)*(x3 - x1) - (y3 - y1)*(x4 - x3)) / d
                            u = ((y2 - y1)*(x3 - x1) - (y3 - y1)*(x2 - x1)) / d

                            if 0 < t and 0 < u and u < 1:

                                x = x1 + t*(x2 - x1) +0.5
                                y = y1 + t*(y2 - y1) +0.5
                                

                                self.intersection = [x + tile["pos"][0]*16, y + tile["pos"][1]*16]
                                self.edge = [(x3, y3), (x4, y4)]
                                self.centroid = [overlap_centroid[0] + tile["pos"][0]*16, overlap_centroid[1] + tile["pos"][1]*16]

                                return True
        return False

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, (self.pos[0] - self.img.get_width()/2 - offset[0],
                            self.pos[1] - self.img.get_height()/2 - offset[1]))
