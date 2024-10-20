import pygame
import json

AUTOTILE_DATAS = {
    tuple(sorted([(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)])): 0,
    tuple(sorted([(0, 1), (1, 0)])): 1,
    tuple(sorted([(0, 1), (-1, 0)])): 2,
    tuple(sorted([(1, 0), (0, -1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(0, 1), (-1, 0), (1, 0)])): 5,
    tuple(sorted([(0, -1), (-1, 0), (1, 0)])): 6,
    tuple(sorted([(0, 1), (1, 0), (0, -1)])): 7,
    tuple(sorted([(0, 1), (-1, 0), (0, -1)])): 8
}

class Tilemap():

    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def autotile(self):
        pass

    def tiles_around(self, pos, NEIGHBOR_OFFSETS):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos, NEIGHBOR_OFFSETS):
        rects = []
        for tile in self.tiles_around(pos, NEIGHBOR_OFFSETS):
            if True:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset = (0, 0)):

        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets["Terrain"][tile["variant"]], (tile["pos"][0] - offset[0], 
                                                                     tile["pos"][1] - offset[1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets["Terrain"][tile["variant"]], (tile["pos"][0]*self.tile_size - offset[0],
                                                                     tile["pos"][1]*self.tile_size - offset[1]))


        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets["Terrain"][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))