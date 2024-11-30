import math
from typing import Tuple

import numpy as np
from PIL import Image

from PIL.Image import Resampling
from moviepy import Effect, VideoClip
from moviepy.Clip import Clip


class ZoomInEffect(Effect):
    def __init__(self, zoom_ratio=0.04):
        self.zoom_ratio = zoom_ratio
        super().__init__()

    def apply(self, clip: Clip) -> VideoClip:
        def transform_frame(get_frame, t: int):
            zoom_factor = t * self.zoom_ratio
            return crop_percent(get_frame(t), 0.5, 0.5, zoom_factor)

        return clip.transform(transform_frame, keep_duration=True)


def crop_percent(src: np.array, x_mid: float, y_mid: float, crop: float):
    # Opens an image in RGB mode
    im = Image.fromarray(src)
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size
    # calculate cut and zoom shenanigans
    image_x, image_y = __get_init_image_margins(width, height)
    new_width, new_height = __calculate_zoom(image_x, image_y, crop)

    # calculate movement room
    pot_x_movement = width - new_width
    pot_y_movement = height - new_height

    # calculate cuts
    left = int(pot_x_movement * x_mid)
    top = int(pot_y_movement * y_mid)
    right = left + new_width
    bot = top + new_height

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bot))

    # resize image for final save
    # width = int((HEIGHT / im1.height) * im1.width)
    buf = np.array(im1.resize((width, height), resample=Resampling.LANCZOS))
    im1.close()
    return buf


def __get_init_image_margins(x_size: int, y_size: int) -> Tuple[int, int]:
    return x_size, y_size
    y_smaller = x_size / RATIO_WIDTH > y_size / RATIO_HEIGHT
    if y_smaller:
        return int((y_size * RATIO_WIDTH / RATIO_HEIGHT)), y_size
    else:
        return x_size, int((x_size / RATIO_WIDTH * RATIO_HEIGHT))


def __calculate_zoom(x_size: int, y_size: int, zoom_factor: float) -> Tuple[int, int]:
    return x_size - (x_size * zoom_factor), y_size - (y_size * zoom_factor)
    new_x_size: int = int(x_size - x_size * math.sqrt(zoom_factor * 0.5))
    #new_x_size -= new_x_size % RATIO_WIDTH
    #return int(new_x_size), int(new_x_size / RATIO_WIDTH * RATIO_HEIGHT)
    return int(x_size), int(y_size)