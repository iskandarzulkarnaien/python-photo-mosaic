import itertools
import random

from skimage import img_as_float
from skimage.metrics import mean_squared_error

def shuffle_first_items(lst, i):
    if not i:
        return lst
    first_few = lst[:i]
    remaining = lst[i:]
    random.shuffle(first_few) 
    return first_few + remaining

def bound(low, high, value):
    return max(low, min(high, value))

def img_mse(im1, im2):
    """Calculates the root mean square error (RSME) between two images"""
    try:
        return mean_squared_error(img_as_float(im1), img_as_float(im2))
    except ValueError:
        print(f'RMS issue, Img1: {im1.size[0]} {im1.size[1]}, Img2: {im2.size[0]} {im2.size[1]}')
        raise KeyboardInterrupt

def resize_box_aspect_crop_to_extent(img, target_aspect, centerpoint=None):
    width = img.size[0]
    height = img.size[1]
    if not centerpoint:
        centerpoint = (int(width / 2), int(height / 2))

    requested_target_x = centerpoint[0]
    requested_target_y = centerpoint[1]
    aspect = width / float(height)
    if aspect > target_aspect:
        # Then crop the left and right edges:
        new_width = int(target_aspect * height)
        new_width_half = int(new_width/2)
        target_x = bound(new_width_half, width-new_width_half, requested_target_x)
        left = target_x - new_width_half
        right = target_x + new_width_half
        resize = (left, 0, right, height)
    else:
        # ... crop the top and bottom: 
        new_height = int(width / target_aspect)
        new_height_half = int(new_height/2)
        target_y = bound(new_height_half, height-new_height_half, requested_target_y)
        top = target_y - new_height_half
        bottom = target_y + new_height_half
        resize = (0, top, width, bottom)
    return resize

def aspect_crop_to_extent(img, target_aspect, centerpoint=None):
    '''
    Crop an image to the desired perspective at the maximum size available.
    Centerpoint can be provided to focus the crop to one side or another - 
    eg just cut the left side off if interested in the right side.

    target_aspect = width / float(height)
    centerpoint = (width, height)
    '''
    resize = resize_box_aspect_crop_to_extent(img, target_aspect, centerpoint)
    return img.crop(resize)

def coords_from_middle(x_count, y_count, y_bias=1, shuffle_first=0, ):
    '''
    Lets start in the middle where we have more images.
    And we dont get "lines" where the same-best images
    get used at the start.

    y_bias - if we are using non-square coords, we can
        influence the order to be closer to the real middle.
        If width is 2x height, y_bias should be 2.

    shuffle_first - We can suffle the first X coords
        so that we dont use all the same-best images
        in the same spot -  in the middle

    from movies.mosaic_mem import coords_from_middle
    x = 10
    y = 10
    coords_from_middle(x, y, y_bias=2, shuffle_first=0)
    '''
    x_mid = int(x_count/2)
    y_mid = int(y_count/2)
    coords = list(itertools.product(range(x_count), range(y_count)))
    coords.sort(key=lambda c: abs(c[0]-x_mid)*y_bias + abs(c[1]-y_mid))
    coords = shuffle_first_items(coords, shuffle_first)
    return coords