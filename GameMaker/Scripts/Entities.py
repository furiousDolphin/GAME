
import pygame


class Entity():

    def __init__(self, game, type, size, pos):
        self.game = game
        self.type = type
        self.size = size
        self.pos = list(pos)
        self.velocity = [0, 0]
        #self.tile_size = game.tilemap.tile_size
        self.tile_size = 16

        self.NEIGHBOR_OFFSETS = []
        
        for x in range(-1, int(size[0]//self.tile_size + 2)):
            for y in range(-1, int(size[1]//self.tile_size + 2)):
                self.NEIGHBOR_OFFSETS.append((x, y))

    def rect(self):
        return pygame.Rect(self.pos, self.size)
    
    def update(self, tilemap, movement=(0, 0, 0, 0)):

        movement_frame = (movement[3] - movement[2] + self.velocity[0],
                          movement[1] - movement[0] + self.velocity[1])
        
        collisions = {"top": False, "bottom": False, "left": False, "right": False}
        
        self.pos[0] += movement_frame[0]
        rect = self.rect()
        for tile_rect in tilemap.physics_rects_around(self.pos, self.NEIGHBOR_OFFSETS):
            if rect.colliderect(tile_rect):
                if movement_frame[0] > 0:
                    collisions["right"] = True
                    rect.right = tile_rect.left
                if movement_frame[0] < 0:
                    collisions["left"] = True
                    rect.left = tile_rect.right                   
                self.pos[0] = rect.x
            

        self.pos[1] += movement_frame[1]
        rect = self.rect()
        for tile_rect in tilemap.physics_rects_around(self.pos, self.NEIGHBOR_OFFSETS):
            if rect.colliderect(tile_rect):
                if movement_frame[1] > 0:
                    collisions["bottom"] = True
                    rect.bottom = tile_rect.top
                if movement_frame[1] < 0:
                    collisions["top"] = True
                    rect.top = tile_rect.bottom                    
                self.pos[1] = rect.y
            
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets["Player"], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
