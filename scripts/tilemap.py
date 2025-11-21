import pygame
import json

# Define offsets for neighboring tiles (used for checking surrounding tiles)
NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

# Define tile types that interact with physics
PHYSICS_TILES = {"stone"}


class TileMap:
    def __init__(self, game, tile_size=16):
        # Reference to the main game instance
        self.game = game
        # Size of each tile in pixels
        self.tile_size = tile_size
        # Dictionary to store tiles on the grid
        self.tile_map = {}
        # List to store tiles that are not aligned to the grid
        self.off_grid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.off_grid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.off_grid_tiles.remove(tile)

        for loc in self.tile_map:
            tile = self.tile_map[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size

                if not keep:
                    del self.tile_map[loc]

        return matches

    def save(self, path):
        file = open(path, 'w')
        json.dump({'tilemap': self.tile_map, 'tile_size': self.tile_size, 'offgrid': self.off_grid_tiles}, file)
        file.close()

    def load(self, path):
        file = open(path, 'r')
        map_data = json.load(file)
        file.close()

        self.tile_map = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.off_grid_tiles = map_data['offgrid']

    def solid_check(self, pos):
        tile_loc = f"{int(pos[0] // self.tile_size)};{int(pos[1] // self.tile_size)}"
        if tile_loc in self.tile_map:
            if self.tile_map[tile_loc]['type'] in PHYSICS_TILES:
                return self.tile_map[tile_loc]

    def physics_rects_around(self, pos):
        # Get rectangles for tiles that interact with physics around a position
        rects = []
        # Grid tiles
        for x in range(int(pos[0] // self.tile_size) - 1, int(pos[0] // self.tile_size) + 2):
            for y in range(int(pos[1] // self.tile_size) - 1, int(pos[1] // self.tile_size) + 2):
                loc = f"{x};{y}"
                if loc in self.tile_map:
                    tile = self.tile_map[loc]
                    if tile['type'] in ['stone']:  # Add all solid types
                        rects.append(pygame.Rect(tile['pos'][0] * self.tile_size + 10,tile['pos'][1] * self.tile_size,
                                                1, 1))
        # Off-grid/large tiles

        for tile in self.off_grid_tiles:
            if tile['type'] in ['stone']:  # Add all solid types
                rects.append(pygame.Rect(tile['pos'][0], tile['pos'][1], 1, 1))
        return rects


    def render(self, surf, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = f"{str(x)};{str(y)}"
                if loc in self.tile_map:
                    tile = self.tile_map[loc]
                    if tile['type'] in ['stone','spawners']:
                        surf.blit(self.game.assets[tile['type']][tile['variant']], (
                        tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        # Render tiles that are not aligned to the grid
        for tile in self.off_grid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
