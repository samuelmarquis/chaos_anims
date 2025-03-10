import os
from pickletools import uint8

import numpy as np
from PIL import Image
from util import sorted_alphanumeric

def mask(source_dir, mask_dir, size):
    n = 0
    for f in sorted_alphanumeric(os.listdir(f"{source_dir}")):
        image = Image.open(f"{source_dir}/{f}")
        image.resize((size,size))
        a = np.array(image.convert('RGB'))

        lb = np.array([0, 0, 0])
        lmb = np.array([10, 10, 10])
        umb = np.array([0, 0, 0])
        ub = np.array([0, 0, 0])

        mask1 = np.all((a < lmb), axis=2)
        #mask2 = np.all((a >= lmb) & (a <= umb), axis=2)
        #mask3 = np.all((a > umb), axis=2)

        a[mask1] = [255, 255, 255]
        a[~mask1] = [0, 0, 0]
        #a[mask2] = [0, 0, 0]
        #a[mask3] = [255, 255, 255]

        Image.fromarray(a).save(f"{mask_dir}/{f}")
        n += 1
        if n % 100 == 0 and n > 0:
            print(f" - masked {n} style images")

if __name__ == '__main__':
    mask("vid_pipe/scream11/style", "vid_pipe/scream11/style_masktest", 512)