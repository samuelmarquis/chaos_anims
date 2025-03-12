import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from util import saturate, grad_map, read_image, write_image


def merge_masks(src_dir, sieve_dir, target_dir, n_layers):
    mask_colors = np.array([
        [0, 0, 0],  # Water & BG
        [0, 38, 89],  # Earth
        [0, 38, 89],  # Platform
        [45, 48, 40],  # Pants
        [255, 255, 255],  # Jacket
        [40, 44, 48],  # Shirt
        [0.5,0.75,1],  # Hands
        [0, 0, 1],  # Face
        [40, 40, 40],  # Hair
        ]) / 255.0

    maps = [
        # Water & BG
        lambda a, c, cnf, msk : np.where(msk > 0, c * cnf, a),
        # Earth
        lambda a, c, cnf, msk : np.where(msk > 0, c * cnf, a),
        # Platform
        lambda a, c, cnf, msk: np.where(msk > 0, saturate(a * c, 4, 0.5), a),
        # Pants
        lambda a, c, cnf, msk: np.where(msk > 0, c * cnf, a),
        # Jacket
        lambda a, c, cnf, msk: np.where(msk > 0, c * cnf, a),
        # Shirt
        lambda a, c, cnf, msk: np.where(msk > 0, c * cnf, a),
        # Hands
        lambda a, c, cnf, msk: np.where(msk > 0, saturate(a * c, 6, 0.25), a),
        # Face
        lambda a, c, cnf, msk: np.where(msk > 0, grad_map(saturate(a, 30, 0.4), [0,0,0],[0.5,0.75,1]), a),
        # Hair
        lambda a, c, cnf, msk: np.where(msk > 0, c * cnf, a)
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
    base = "scream1"
    sub = "a"
    full = f"vid_pipe/{base}/{sub}"
    merge_masks(f"{full}_src_frames",
                f"{full}_sieve",
                f"{full}_masks", 9)