import os
from time import sleep
from PIL import Image
from util import sorted_alphanumeric
from video_editor import crop_framesplit
#from segment import segment_bw, segment_anything
from sieve_to_mask import merge_masks
from fractal_mask import mask
from ebsynth import ebsynth_wrapper
from ffmpeg_wrapper import ffmpeg_wrapper
from os import makedirs
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import Process

pname = "scream"
pidx = 5
suff = None

base = "vid_pipe"
name = f"{pname}{pidx}"
pdir = f"{base}/{name}"

audio_name = f"audio/{pname}/{pidx}s.wav"
res = 1024

def do_it(s):
    prefix = ("" if s is None else f"{s}_")
    flatten = partial(merge_masks,f"{pdir}/{prefix}src_frames", f"{pdir}/{prefix}sieve", f"{pdir}/{prefix}masks", 16)
    proc = Process(target=flatten)
    proc.start()
    #sleep(10)
    #print("Starting ebsynth")
    #ebsynth_wrapper(f"{pdir}/style",
    #                f"{pdir}/style",
    #                f"{pdir}/{s}masks",
    #                f"{pdir}/{s}output")
    return s

if __name__ == "__main__":
    makedirs(f"{pdir}/style", exist_ok=True)
    makedirs(f"{pdir}/style_masks", exist_ok=True)

    if suff is None:
        makedirs(f"{pdir}/src_frames", exist_ok=True)
        makedirs(f"{pdir}/masks", exist_ok=True)
        makedirs(f"{pdir}/output", exist_ok=True)
        makedirs(f"{pdir}/sieve", exist_ok=True)

    else:
        for s in suff:
            makedirs(f"{pdir}/{s}_src_frames", exist_ok=True)
            makedirs(f"{pdir}/{s}_masks", exist_ok=True)
            makedirs(f"{pdir}/{s}_output", exist_ok=True)
            makedirs(f"{pdir}/{s}_sieve", exist_ok=True)

    needed = [None]

    with ProcessPoolExecutor() as pool:
        for s in pool.map(do_it, needed):
            print(f"Finished {name}{s}")
            ffmpeg_wrapper(f"{pdir}/{s}_output",
                           audio_name,
                           f"{pname}{pidx}{s}_1",
                           framerate=24,
                           pattern="%05d",
                           comp_rat=20)