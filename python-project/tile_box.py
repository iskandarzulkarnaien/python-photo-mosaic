import time

import numpy as np
from PIL import Image

from progress_counter import ProgressCounter
from utils import aspect_crop_to_extent, img_mse

class TileBox:
    """
    Container to import, process, hold, and compare all of the tiles 
    we have to make the mosaic with.
    """
    def __init__(self, tile_paths, config):
        self.config = config
        self.tiles = list()
        self.prepare_tiles_from_paths(tile_paths)
        self.valid_indices = set(range(len(self.tiles)))
        print(len(self.valid_indices))
        
    def __process_tile(self, tile_path):
        with Image.open(tile_path) as i:
            img = i.copy()
        img = aspect_crop_to_extent(img, self.config.tile_ratio)
        large_tile_img = img.resize(self.config.tile_size, Image.ANTIALIAS).convert(self.config.color_mode)
        self.tiles.append(large_tile_img)
        return True

    def prepare_tiles_from_paths(self, tile_paths):
        print('Reading tiles from provided list...')
        progress = ProgressCounter(len(tile_paths))
        for tile_path in tile_paths:
            progress.update()
            self.__process_tile(tile_path)          
        print('Processed tiles.')
        return True

    def best_tile_block_match(self, tile_block_original):
        # match_results = [img_mse(t, tile_block_original) for t in self.tiles] 
        # best_fit_tile_index = np.argmin(match_results)

        # # match_results = [(img_mse(self.tiles[i], tile_block_original), i) for i in self.valid_indices] 
        # # best_fit_tile_index = min(match_results, key=lambda t: t[0])[1]

        best_fit_tile_index = None
        best_min = float('inf')
        for i in self.valid_indices:
            t = self.tiles[i]
            curr_min = img_mse(t, tile_block_original)
            if curr_min < best_min:
                best_fit_tile_index = i
                best_min = curr_min

        return best_fit_tile_index

    def best_tile_from_block(self, tile_block_original, reuse=False):
        if not self.tiles:
            print('Ran out of images.')
            raise KeyboardInterrupt
        
        # start_time = time.time()
        i = self.best_tile_block_match(tile_block_original)
        # print("BLOCK MATCH took --- %s seconds ---" % (time.time() - start_time))
        match = self.tiles[i].copy()
        if not reuse:
            # del self.tiles[i]
            self.valid_indices.remove(i)
        return match
