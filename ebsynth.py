import os
import subprocess
from util import sorted_alphanumeric
from threading import Thread
from time import sleep

def ebsynth_wrapper(style_dir, style_mask_dir, guide_mask_dir, output_dir):
    def ebcall(n,f):
        s,sm,gm = f
        args = ['./ebsynth/bin/ebsynth.exe', '-backend', 'cuda',
                '-style', f'{style_dir}/{s}',
                '-guide', f'{style_mask_dir}/{sm}', f'{guide_mask_dir}/{gm}',
                '-output', f'{output_dir}/{n:05d}.png']
        subprocess.run(args)
        return f"Finished frame {n:05d}"

    for n,f in enumerate(zip(sorted_alphanumeric(os.listdir(style_dir)),
                             sorted_alphanumeric(os.listdir(style_mask_dir)),
                             sorted_alphanumeric(os.listdir(guide_mask_dir)))):
        ebcall(n,f)




if __name__ == '__main__':
    base = "scream2"
    sub = ""  # Don't forget the _
    full = f"{base}{sub}"
    ebsynth_wrapper(f"vid_pipe/{base}/style",
                    f"vid_pipe/{base}/style_masks",
                    f"vid_pipe/{base}/{sub}masks",
                    f"vid_pipe/{base}/{sub}output")