from os import listdir, chdir
from pathlib import Path
import subprocess

from tqdm import tqdm

from util import sorted_alphanumeric
from threading import Thread
from time import sleep

which = "scream9"

def ebsynth_wrapper(sd, md, gd, od):
    print(f"Starting ebsynth ({which}):")
    print(f" - style={sd}")
    print(f" - md={md} : gd={gd}")
    print(f" - out={od}")
    def ebcall(n,f):
        s,m,g = f
        args = ['../../ebsynth/bin/ebsynth.exe', '-backend', 'cuda',
                '-style', f'{sd}/{s}',
                '-guide', f'{md}/{m}', f'{gd}/{g}',
                '-output', f'{od}/{n:05d}.png']
        subprocess.run(args, stdout=subprocess.DEVNULL)
        return f"Finished frame {n:05d}"

    for n,f in tqdm(enumerate(zip(sorted_alphanumeric(listdir(sd)),
                                  sorted_alphanumeric(listdir(md)),
                                  sorted_alphanumeric(listdir(gd)),
                                  ))):
        #if n<???:
        #   continue

        #pf = Path(f"{od}/{n:05d}.png")
        #if pf.exists():
        #    continue
        #print(f"regenerating {n}")

        ebcall(n,f)

def ebsynth2_wrapper(sd, m1d, g1d, m2d, g2d, od):
    print("Starting ebsynth:")
    print(f" - style={sd}")
    print(f" - m1d={m1d} : g1d={g1d}")
    print(f" - m2d={m2d} : g2d={g2d}")
    print(f" - out={od}")
    def ebcall(n,f):
        s,m1,g1,m2,g2 = f
        args = ['../../ebsynth/bin/ebsynth.exe', '-backend', 'cuda',
                '-style', f'{sd}/{s}',
                '-guide', f'{m1d}/{m1}', f'{g1d}/{g1}',
                '-guide', f'{m2d}/{m2}', f'{g2d}/{g2}',
                '-output', f'{od}/{n:05d}.png']
        subprocess.run(args, stdout=subprocess.DEVNULL)
        return f"Finished frame {n:05d}"

    for n,f in tqdm(enumerate(zip(sorted_alphanumeric(listdir(sd)),
                             sorted_alphanumeric(listdir(m1d)),
                             sorted_alphanumeric(listdir(g1d)),
                             sorted_alphanumeric(listdir(m2d)),
                             sorted_alphanumeric(listdir(g2d))))):
        ebcall(n,f)

if __name__ == '__main__':
    chdir(f"vid_pipe/{which}")
    ebsynth_wrapper("style1", "style2", "src_frames", "output1")
    #ebsynth2_wrapper("style", "style", "masks3", "depth_masks", "depth", "output3")