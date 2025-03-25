from os import listdir, makedirs, chdir
from shutil import copyfile
import numpy as np
from tqdm import tqdm

from util import read_image, write_image, noise, saturate, grad_map, edge_detect, sorted_alphanumeric, channel_saturate, \
    write_image2, read_image2

which = "scream11"

def dual_cutout():
    chdir(f"vid_pipe/{which}")
    for n, (s, st) in tqdm(enumerate(zip(listdir("output2"), listdir("output4")))):
        s1   = read_image2(f"sieve/masks/mask_{n}_1.png")
        s2 = read_image2(f"sieve/masks/mask_{n}_2.png")
        s3 = read_image2(f"sieve/masks/mask_{n}_3.png")
        a = read_image2(f"output2/{s}")
        ol = read_image2(f"output4/{st}")
        a = np.where(s1 > 0, ol, a)
        a = np.where(s2 > 0, ol, a)
        a = np.where(s3 > 0, ol, a)
        write_image(f"output1/{n:05d}.png", a)

def fix_times():
    chdir(f"vid_pipe/{which}")
    makedirs("style_masks2", exist_ok=True)
    for n,f in tqdm(enumerate(listdir("style_masks2_old"))):
        if n<24:
            continue
        copyfile(f"style_masks2_old/{f}", f"style_masks2/{n-24:05d}.png")

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
    chdir(f"vid_pipe/{which}")
    for n,s in enumerate(tqdm(listdir("in_clip/"))):
        a = read_image2(f"in_clip/{s}")# * read_image2(f"depth/{n:08d}.png")
        a = np.where((read_image2(f"clip_mask/mask_{1 if n==0 else n}_1.png").astype(np.bool)) > 0, [0,0,0], a)
        #s = np.where(read_image2(f"sieve/masks/mask_{n}_6.png")>0, s-0.12, s) # skin
        #a = read_image2(f"style/{s}")
        #a = grad_map(a, [0,0,0],[1,1,1])
        write_image(f"out_clip/{n:05d}.png", a)

if __name__ == "__main__":
   map_folder()
