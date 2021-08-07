# 05. get_ram.py
import retro
import numpy as np

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

ram = env.get_ram()

full_screen_tiles = ram[0x0500:0x069F+1]

# print(full_screen_tiles.shape)
# print(full_screen_tiles)

full_screen_tile_count = full_screen_tiles.shape[0]

full_screen_page1_tile = full_screen_tiles[:full_screen_tile_count//2].reshape((13, 16))
full_screen_page2_tile = full_screen_tiles[full_screen_tile_count//2:].reshape((13, 16))

print(full_screen_page1_tile)
print(full_screen_page2_tile)

full_screen_tiles = np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1)

print(full_screen_tiles)
