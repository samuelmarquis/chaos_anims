import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from util import saturate, grad_map, read_image, write_image, channel_saturate, noise, read_image2


def merge_masks(src_dir, sieve_dir, target_dir, n_layers):
    mask_colors = np.array([
        [0, 0, 0], # grass
        [0, 1, 1], # black
        [0, 0, 1], # coat
        [0, 1, 0], # pants
        [1, 1, 0], # shirt
        [0, 1, 0], # skin
        [0, 1, 1], # hair
        ])
    sat_h = [8,10,12]
    sat_c = [0.5,0.5,0.5]
    maps = [
        lambda a, c, cnf, msk: np.where (msk > 0, c, a),# grass
        lambda a, c, cnf, msk: np.where (msk > 0, c, a),# black
        lambda a, c, cnf, msk: np.where (msk > 0, c, a),# coat
        lambda a, c, cnf, msk: np.where(msk > 0, saturate(noise(a,1),20,0), a),# pants
        lambda a, c, cnf, msk: np.where(msk > 0, saturate(noise(a,1),20,0), a),# shirt
        lambda a, c, cnf, msk: np.where (msk > 0, grad_map(saturate(a,16,0.35), [0,0,0], [1,1,1]), a),# skin
        lambda a, c, cnf, msk: np.where (msk > 0, grad_map(saturate(a,16,0.35), [0,0,0], [1,1,1]), a),# hair
    ]

    def frame(nf):
        n, f = nf
        a = read_image2(f"{src_dir}/{f}")
        if a is None:
            print(f"Missing {f}")
            return n
        layer_with = partial(layer, n)
        with ThreadPoolExecutor(max_workers=n_layers) as pool2:
            fres = pool2.map(layer_with, range(1, n_layers + 1))
            for m, cnfmsk in enumerate(fres):
                if cnfmsk is None:
                    return n
                cnf, msk = cnfmsk
                c = mask_colors[m]
                a = maps[m](a,c,cnf,msk)
        write_image(os.path.join(target_dir, f"{n:05d}.png"), np.minimum(a, 1, None))
        return n

    def layer(n, m):
        cnf = read_image2(f"{sieve_dir}/confidences/confidences_{n}_{m}.png")
        msk = read_image2(f"{sieve_dir}/masks/mask_{n}_{m}.png")
        if cnf is None or msk is None:
            return None
        return cnf, msk

    with ThreadPoolExecutor(max_workers=50) as pool:
        print("Creating pool... pool...")
        res = pool.map(frame, enumerate(os.listdir(src_dir)))
        for n in res:
            if n % 100 == 0 and n > 0:
                print(f"Merged ~{n} masks to {target_dir}")


if __name__ == '__main__':
    base = "scream9"
    sub = ""
    full = f"vid_pipe/{base}/{sub}"
    merge_masks(f"{full}src_frames",
                f"{full}sieve",
                f"{full}masks3", 7)