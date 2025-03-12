import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from util import saturate, grad_map, read_image, write_image, channel_saturate


def merge_masks(src_dir, sieve_dir, target_dir, n_layers):
    mask_colors = np.array([
        # water
        [0, 1, 0.5],
        # concrete
        [0.6, 0.5, 0.7],
        # railing
        [0, 0, 0],
        # hill
        [0.6, 0.7, 0.4],
        # treeline lower
        [0.7, 0.8, 0.5],
        # treeline upper
        [0.8, 0.9, 0.6],
        # sky
        [0, 1, 1],
        # dasha jacket & hat
        [1.0, 0.0, 1],
        # dasha pants
        [0.8, 0.6, 0.8],
        # dasha hair
        [1, 1, 1],
        # dasha skin
        [0.9, 0.8, 0.7],
        # sam jacket
        [1, 1, 1],
        # guitar
        [0.8, 0.5, 0.5],
        # sam pants and shirt
        [0, 0, 0],
        # sam skin
        [0.35, 1, 0.3],
        # sam hair
        [0.5, 0.5, 1],
        ])
    sat_h = [8,10,12]
    sat_c = [0.5,0.5,0.5]
    maps = [
        lambda a, c, cnf, msk: np.where(msk > 0, a * c, a),
        lambda a, c, cnf, msk: channel_saturate(a, [14, 12, 16], [0.6, 0.57, 0.5]),
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: np.where(msk > 0, a * c, a),
        lambda a, c, cnf, msk: np.where(msk > 0, a * c, a),
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
        lambda a, c, cnf, msk: a,
    ]

    def frame(nf):
        n, f = nf
        a = read_image(f"{src_dir}/{f}")
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
        cnf = read_image(f"{sieve_dir}/confidences/confidences_{n}_{m}.png")
        msk = read_image(f"{sieve_dir}/masks/mask_{n}_{m}.png")
        if cnf is None or msk is None:
            return None
        return cnf, msk

    with ThreadPoolExecutor(max_workers=50) as pool:
        print("Creating pool... pool...")
        res = pool.map(frame, enumerate(os.listdir(src_dir)))
        for n in res:
            if n % 100 == 0 and n > 0:
                print(f"Merged ~{n} masks to {target_dir}")

        """
        # Water
        if m==1:
            a = np.where(msk > [0,0,0], ca, a)

        # Earth
        if m==2:
            a = np.where(cf > [0,0,0], a*c, a)

        # Platform
        if m==3:
            a = np.where(cf > [0,0,0])

        # Pants
        if m == 4:
            None

        #Jacket
        c = [1,0,0]
        if m==5:
            ca = (a**0.5) * c
            a = np.where(cf > [0.0, 0.0, 0.0], ca, a)

        # Shirt
        c = [1,1,0]
        if m==6:
            a = np.where(cf > [0, 0, 0], c, a)

        # Hands
        if m==7:
            None

        # Face
        c = [0.8,0.7,0.7]
        if m==8:
            ca = (np.tanh(((-a+1) * c + 0.1) * 10 - 6) + 1) / 2
            #ca = a * c
            a = np.where(cf > [0, 0, 0], ca, a)

        #Hair
        c = [0,4,0]
        if m==9:
            a = np.where(cf > [0, 0, 0], a * c, a)
        """


if __name__ == '__main__':
    base = "scream2"
    sub = ""
    full = f"vid_pipe/{base}/{sub}"
    merge_masks(f"{full}src_frames",
                f"{full}sieve",
                f"{full}masks", 16)