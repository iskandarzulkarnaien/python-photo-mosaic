from config import Config
from mosaic_image import MosaicImage
from progress_counter import ProgressCounter
from source_image import SourceImage
from tile_box import TileBox
from utils import coords_from_middle

import time

def create_mosaic(source_path, target, tile_ratio=1920/800, tile_width=75, enlargement=8, reuse=True, color_mode='RGB', tile_paths=None, shuffle_first=30):
    """Forms an mosiac from an original image using the best
    tiles provided. This reads, processes, and keeps in memory
    a copy of the source image, and all the tiles while processing.

    Arguments:
    source_path -- filepath to the source image for the mosiac
    target -- filepath to save the mosiac
    tile_ratio -- height/width of mosaic tiles in pixels
    tile_width -- width of mosaic tiles in pixels
    enlargement -- mosaic image will be this many times wider and taller than the original
    reuse -- Should we reuse tiles in the mosaic, or just use each tile once?
    color_mode -- L for greyscale or RGB for color
    tile_paths -- List of filepaths to your tiles
    shuffle_first -- Mosiac will be filled out starting in the center for best effect. Also, 
        we will shuffle the order of assessment so that all of our best images aren't 
        necessarily in one spot.
    """
    config = Config(
        tile_ratio = tile_ratio,		# height/width of mosaic tiles in pixels
        tile_width = tile_width,		# height/width of mosaic tiles in pixels
        enlargement = enlargement,	    # the mosaic image will be this many times wider and taller than the original
        color_mode = color_mode,	    # L for greyscale or RGB for color
    )
    # Pull in and Process Original Image
    print('Setting Up Target image')
    source_image = SourceImage(source_path, config)

    # Setup Mosaic
    mosaic = MosaicImage(source_image.image, target, config)

    # Assest Tiles, and save if needed, returns directories where the small and large pictures are stored
    print('Assessing Tiles')
    tile_box = TileBox(tile_paths, config)

    try:
        progress = ProgressCounter(mosaic.total_tiles)
        for x, y in coords_from_middle(mosaic.x_tile_count, mosaic.y_tile_count, y_bias=config.tile_ratio, shuffle_first=shuffle_first):
            progress.update()

            # Make a box for this sector
            box_crop = (x * config.tile_width, y * config.tile_height, (x + 1) * config.tile_width, (y + 1) * config.tile_height)

            # Get Original Image Data for this Sector
            comparison_block = source_image.image.crop(box_crop)

            # Get Best Image name that matches the Orig Sector image

            start_time = time.time()
            tile_match = tile_box.best_tile_from_block(comparison_block, reuse=reuse)
            print("TILE MATCH took --- %s seconds ---" % (time.time() - start_time))
            
            # Add Best Match to Mosaic
            mosaic.add_tile(tile_match, box_crop)

            # Saving Every Sector
            mosaic.save() 

    except KeyboardInterrupt:
        print('\nStopping, saving partial image...')

    finally:
        mosaic.save()

from os import walk
import random

def main():
    folder_name = 'birds_11788'
    filenames = next(walk(folder_name), (None, None, []))[2]  # [] if no file
    filenames = [f'{folder_name}/{filename}' for filename in filenames]

    # random.seed(123)
    # filenames = random.sample(filenames, 1000)

    start_time = time.time()
    create_mosaic('bird.jpg', 'out.jpg', 1920/800, 75, 1, False, 'RGB', filenames)
    print("MOSAIC CREATION took --- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
