from os import listdir, chdir
from pathlib import Path
import subprocess

from tqdm import tqdm

from util import sorted_alphanumeric
from threading import Thread
from time import sleep

which = "scream6"

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

    for n, f in enumerate(tqdm(zip(sorted_alphanumeric(listdir(sd)),
                                   sorted_alphanumeric(listdir(md)),
                                   sorted_alphanumeric(listdir(gd)),
                                   ))):
        #if n<310:
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

    for n,f in enumerate(tqdm(zip(sorted_alphanumeric(listdir(sd)),
                             sorted_alphanumeric(listdir(m1d)),
                             sorted_alphanumeric(listdir(g1d)),
                             sorted_alphanumeric(listdir(m2d)),
                             sorted_alphanumeric(listdir(g2d))))):
        ebcall(n,f)

if __name__ == '__main__':
    chdir(f"vid_pipe/{which}")
    for _n in range(8):
        n = _n+1
        __import__("os").makedirs(f"ot{n}", exist_ok=True)
        ebsynth_wrapper("../../finished_frameseqs/scream/3t/", "../../finished_frameseqs/scream/3t/", f"t{n}", f"ot{n}")
    #ebsynth2_wrapper("style", "style_masks", "masks1", "depth_masks", "depth", "output4")
    #ebsynth2_wrapper("style", "style", "masks3", "depth_masks", "depth", "output3")