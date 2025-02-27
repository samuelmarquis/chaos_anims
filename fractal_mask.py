import os
import numpy as np
from PIL import Image
from util import sorted_alphanumeric

def mask(source_dir, mask_dir, size):
    n = 0
    for f in sorted_alphanumeric(os.listdir(f"{source_dir}")):
        image = Image.open(f"{source_dir}/{f}")
        image.resize((size,size))
        a = np.array(image.convert('RGB'))

        lower_bound = np.array([0, 0, 0])
        upper_bound = np.array([200, 200, 255])

        mask = np.all((a >= lower_bound) & (a <= upper_bound), axis=2)
        a[~mask] = [0, 0, 0]
        a[mask] = [255, 255, 255]

        Image.fromarray(a).save(f"{mask_dir}/{f}")
        n += 1
        if n % 100 == 0 and n > 0:
            print(f" - masked {n} style images")