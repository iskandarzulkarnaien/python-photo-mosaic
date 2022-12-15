class MosaicImage:
    """Holder for the mosaic"""
    def __init__(self, original_img, target, config):
        self.config = config
        self.target = target
        # Lets just start with original image, scaled up, instead of a blank one
        self.image = original_img
        # self.image = Image.new(original_img.mode, original_img.size)
        self.x_tile_count = int(original_img.size[0] / self.config.tile_width)
        self.y_tile_count = int(original_img.size[1] / self.config.tile_height)
        self.total_tiles  = self.x_tile_count * self.y_tile_count
        print(f'Mosaic will be {self.x_tile_count:,} tiles wide and {self.y_tile_count:,} tiles high ({self.total_tiles:,} total).')

    def add_tile(self, tile, coords):
        """Adds the provided image onto the mosiac at the provided coords."""
        try:
            self.image.paste(tile, coords)
        except TypeError as e:
            print('Maybe the tiles are not the right size. ' + str(e))

    def save(self):
        self.image.save(self.target)

