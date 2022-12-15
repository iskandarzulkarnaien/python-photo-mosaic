from PIL import Image

class SourceImage:
    """Processing original image - scaling and cropping as needed."""
    def __init__(self, image_path, config):
        print('Processing main image...')
        self.image_path = image_path
        self.config = config

        with Image.open(self.image_path) as i:
            img = i.copy()
        w = img.size[0] * self.config.enlargement
        h = img.size[1]	* self.config.enlargement
        large_img = img.resize((w, h), Image.ANTIALIAS)
        w_diff = (w % self.config.tile_width)/2
        h_diff = (h % self.config.tile_height)/2
        
        # if necesary, crop the image slightly so we use a 
        # whole number of tiles horizontally and vertically
        if w_diff or h_diff:
            large_img = large_img.crop((w_diff, h_diff, w - w_diff, h - h_diff))

        self.image =  large_img.convert(self.config.color_mode)
        print('Main image processed.')

