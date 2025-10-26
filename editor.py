import pygame
import sys

# Import utility functions and classes for loading images, entities, and tilemaps
from scripts.utils import load_images,load_image
from scripts.tilemap import TileMap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        pygame.display.set_caption("editor")  # Set the window title
        self.screen = pygame.display.set_mode((1024, 768))  # Main game window
        self.display = pygame.Surface((512, 384))  # Internal display for scaling
        self.clock = pygame.time.Clock()  # Clock to control the frame rate
        self.movement = [False, False, False, False]  # Movement flags for left and right
        self.location = "town"

        # Load game assets (player sprite, tiles, etc.)
        self.assets = {
            'terrain': load_images('tiles/terrain'),
            'decor': load_images('tiles/decor'),
            'large_decor': load_images('tiles/large_decor'),
            'bed': load_images('tiles/bed'),
            'toilet': load_images('tiles/toilet'),
            'furniture': load_images('tiles/furniture'),
            'structure': load_images('tiles/structure'),
            'wall': load_images('tiles/wall'),
            'rug': load_images('tiles/rug'),
            'shelve': load_images('tiles/shelve'),
            'sofas': load_images('tiles/sofas'),
            'painting': load_images('tiles/painting'),
            'fireplace': load_images('tiles/fireplace'),
            'stone': load_images('tiles/stone'),
            'building': load_images('tiles/building'),
            'spawners': load_images('tiles/spawners')

        }

        self.tile_map = TileMap(self, tile_size=16)

        try:
            self.tile_map.load(f'data/maps/{self.location}.json')
        except FileNotFoundError:
            pass

        # Camera scroll offset
        self.scroll = [0, 0]
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False
        self.on_grid = True
        self.size = (0,0)






    def run(self):
        # Main game loop
        while True:
            # Fill the display with a sky-blue background color
            self.display.fill((0,0,0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # changes the scroll values to integers to improve accuracy

            bg_x = -int(render_scroll[0])  # 0.5 for slower parallax, use 1 for 1:1 scroll
            bg_y = -int(render_scroll[1])

            self.display.blit(load_image(f'{self.location}.jpg'),(bg_x,bg_y))
            self.tile_map.render(self.display,offset=render_scroll)
            # Preview
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            m_pos = pygame.mouse.get_pos()
            m_pos = (m_pos[0]/ RENDER_SCALE, m_pos[1]/ RENDER_SCALE)
            tile_pos = (int((m_pos[0] + self.scroll[0]) // self.tile_map.tile_size), int((m_pos[1] + self.scroll[1]) // self.tile_map.tile_size))
            if self.on_grid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tile_map.tile_size - self.scroll[0], tile_pos[1] * self.tile_map.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, m_pos)
            if self.clicking and self.on_grid:
                self.tile_map.tile_map[f"{str(tile_pos[0])};{str(tile_pos[1])}"] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos':tile_pos}

            if self.right_clicking:
                tile_loc = f"{str(tile_pos[0])};{str(tile_pos[1])}"
                if tile_loc in self.tile_map.tile_map:
                    del self.tile_map.tile_map[tile_loc]
                for tile in self.tile_map.off_grid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(m_pos):
                        self.tile_map.off_grid_tiles.remove(tile)


            self.display.blit(current_tile_img, (5,5))

            # Handle events (e.g., quitting, key presses)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.on_grid:
                            for tile in self.tile_map.off_grid_tiles.copy():
                                tile_img = self.assets[tile['type']][tile['variant']]
                                self.size = (tile_img.get_width(), tile_img.get_height())
                            self.tile_map.off_grid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (m_pos[0] + self.scroll[0], m_pos[1] + self.scroll[1]), 'size': self.size})
                    if event.button == 3:
                        self.right_clicking = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False



                if event.type == pygame.KEYDOWN:  # Handle key presses
                    if event.key == pygame.K_a:  # Move left
                        self.movement[0] = True
                    if event.key == pygame.K_d:  # Move right
                        self.movement[1] = True
                    if event.key == pygame.K_w:  # Jump
                        self.movement[2] = True
                    if event.key == pygame.K_s:  # Jump
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid

                    if event.key == pygame.K_o:
                        self.tile_map.save(f'data/maps/{self.location}.json')


                    if event.key == pygame.K_DOWN:
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_UP:
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0

                    if event.key == pygame.K_LEFT:
                        self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    if event.key == pygame.K_RIGHT:
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])

                if event.type == pygame.KEYUP:  # Handle key releases
                    if event.key == pygame.K_a:  # Move left
                        self.movement[0] = False
                    if event.key == pygame.K_d:  # Move right
                        self.movement[1] = False
                    if event.key == pygame.K_w:  # Jump
                        self.movement[2] = False
                    if event.key == pygame.K_s:  # Jump
                        self.movement[3] = False


            # Scale the internal display to fit the main screen and update the display
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            # Cap the frame rate to 60 FPS
            self.clock.tick(60)

# Create a Game instance and start the game loop
game = Editor()
game.run()
