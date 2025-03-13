from os import listdir
import numpy as np
from tqdm import tqdm

from util import read_image, write_image, noise, saturate, grad_map, edge_detect

if __name__ == "__main__":
    for n, (s, st) in tqdm(enumerate(zip(listdir("vid_pipe/scream2/test_out4"), listdir("vid_pipe/scream2/style")))):
        sam   = read_image(f"vid_pipe/scream2/sieve_broad/masks/mask_{n}_2.png")
        dasha = read_image(f"vid_pipe/scream2/sieve_broad/masks/mask_{n}_1.png")
        a = read_image(f"vid_pipe/scream2/test_out4/{s}")
        ol = read_image(f"vid_pipe/scream2/style/{st}")
        se = edge_detect(sam, 3)
        de = edge_detect(dasha, 3)
        a = np.where(se > 0, ol, a)
        a = np.where(de > 0, ol, a)
        write_image(f"vid_pipe/scream2/test_out/{n:05d}.png", a)