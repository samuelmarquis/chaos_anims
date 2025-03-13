from os import listdir
import numpy as np
from tqdm import tqdm

from util import read_image, write_image, noise, saturate, grad_map, edge_detect, sorted_alphanumeric, channel_saturate, \
    write_image2, read_image2


def dual_cutout():
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

def concat():
    n = 0
    for d in sorted_alphanumeric(listdir(f"vid_pipe/scream3/depth/")):
        print(d)
        for di in listdir(f"vid_pipe/scream3/depth/{d}/"):
            print(di)
            a = read_image(f"vid_pipe/scream3/depth/{d}/{di}")
            write_image(f"vid_pipe/scream3/depth/{n:05d}.png", a)
            n += 1

def map_folder():
    for n,s in enumerate(listdir("vid_pipe/scream3/src_frames/")):
        s = read_image2(f"vid_pipe/scream3/src_frames/{s}")
        a = channel_saturate(s, [])
        write_image(f"vid_pipe/scream3/style_masks/{n:05d}.png", a)
        if n%50==0 and n>0:
            print(f"Processed {n} images")

if __name__ == "__main__":
   map_folder()
