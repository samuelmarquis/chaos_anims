import os
import numpy as np
from PIL import Image
from util import sorted_alphanumeric

def mask(source_dir, mask_dir):
    for f in sorted_alphanumeric(os.listdir(f"{source_dir}")):
        image = Image.open(f"{source_dir}/{f}")
        n = np.array(image)

        lower_red = np.array([200, 200, 0])
        upper_red = np.array([255, 255, 100])

        mask = np.all((n >= lower_red) & (n <= upper_red), axis=2)
        n[~mask] = [0,0,0]
        n[mask] = [255,255,255]

        Image.fromarray(n).save(f"{mask_dir}/{f}")