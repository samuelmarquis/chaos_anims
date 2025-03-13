import os
import subprocess

from tqdm import tqdm

from util import sorted_alphanumeric
from threading import Thread
from time import sleep

def ebsynth_wrapper(style_dir, style_mask_dir, guide_mask_dir, output_dir):
    def ebcall(n,f):
        s,sm,gm,dm = f
        args = ['./ebsynth/bin/ebsynth.exe', '-backend', 'cuda',
                '-style', f'{style_dir}/{s}',
                '-guide', f'{style_mask_dir}/{sm}', f'{guide_mask_dir}/{gm}',
                '-output', f'{output_dir}/{n:05d}.png']
        subprocess.run(args, stdout=None)
        return f"Finished frame {n:05d}"

    for n,f in tqdm(enumerate(zip(sorted_alphanumeric(os.listdir(style_dir)),
                             sorted_alphanumeric(os.listdir(style_mask_dir)),
                             sorted_alphanumeric(os.listdir(guide_mask_dir))))):
        ebcall(n,f)

def ebsynth2_wrapper(base_dir, output_dir):
    def ebcall(n,f):
        s,sm,gm,dm,gdm = f
        args = ['./ebsynth/bin/ebsynth.exe', '-backend', 'cuda',
                '-style', f'{base_dir}/style2/{s}',
                '-guide', f'{base_dir}/style_masks2/{sm}', f'{base_dir}/masks2/{gm}',
                '-guide', f'{base_dir}/style_masks/{dm}', f'{base_dir}/depth/{gdm}',
                '-guide', f'{base_dir}/style/{s}', f'{base_dir}/masks/{n}.png',
                '-output', f'{output_dir}/{n:05d}.png']
        subprocess.run(args, stdout=subprocess.DEVNULL)
        return f"Finished frame {n:05d}"

    for n,f in enumerate(zip(sorted_alphanumeric(os.listdir(f"{base_dir}/style2")),
                             sorted_alphanumeric(os.listdir(f"{base_dir}/style_masks2")),
                             sorted_alphanumeric(os.listdir(f"{base_dir}/masks2")),
                             sorted_alphanumeric(os.listdir(f"{base_dir}/style_masks")),
                             sorted_alphanumeric(os.listdir(f"{base_dir}/depth")))):
        ebcall(n,f)


if __name__ == '__main__':
    base = "scream3"
    sub = ""  # Don't forget the _
    full = f"{base}{sub}"
    #ebsynth_wrapper(f"vid_pipe/{base}/style2",
    #                f"vid_pipe/{base}/style_masks",
    #                f"vid_pipe/{base}/depth",
    #                f"vid_pipe/{base}/{sub}output")
    ebsynth2_wrapper(f"vid_pipe/{base}", f"vid_pipe/{base}/output")