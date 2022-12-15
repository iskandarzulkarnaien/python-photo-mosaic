class Config:
    def __init__(self, tile_ratio=1920/800, tile_width=50, enlargement=8, color_mode='RGB'):
        self.tile_ratio = tile_ratio # 2.4
        self.tile_width = tile_width # height/width of mosaic tiles in pixels
        self.enlargement = enlargement # mosaic image will be this many times wider and taller than original
        self.color_mode = color_mode # mosaic image will be this many times wider and taller than original

    @property
    def tile_height(self):
        return int(self.tile_width / self.tile_ratio)

    @property
    def tile_size(self):
        return self.tile_width, self.tile_height # PIL expects (width, height)
