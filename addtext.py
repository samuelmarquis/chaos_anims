import os
import numpy as np
import xml.etree.ElementTree as ET
from parameters import *
from diffusers.utils import load_image
import itertools
import sys
np.set_printoptions(threshold=sys.maxsize)

class iterator:
    def __init__(self, name):
        self.name = name
        self.xangle = None
        self.yangle = None
        self.xlen = None
        self.ylen = None
        self.offset = None
        self.palette_index = None
        self.transforms = {}

title = "scream"
number = 4
name = f"{title}_{number}"
stemprefixes = ["b", "p"]

audiopath = f"audio/{name}.wav"
flamepath = f"chaos/{name}.chaos"

print(f"Loading {audiopath}")

song, sr, _, duration_f, duration_s = load_song(audiopath)
stemnames = []
stems = {}
for s in stemprefixes:
    stemnames.append(f"audio/{title}{s}_{number}.wav")
    stems[s] = load_song(stemnames[-1])[0] #if you render stems at a different SR you're cooked

print(f"Successfully read song data, sample rate = {sr}, clip is {duration_f} frames and {duration_s} seconds long. Computing flows...")
for s in stemnames:
    print(f"Read stem: {s}")

flows = compute_flows(song, sr)
sflows = {}
for p in stemprefixes:
    sflows[p] = compute_flows(stems[p], sr)

counter = 0
toggle = 0
othercounter = 0
for f in os.listdir('finished_frameseqs/old/scream_4'):
    image = load_image(f"finished_frameseqs/scream_4/{f}")
    if (sflows['p']["rms"][counter] < 0.45) or othercounter > 41:
        if toggle == 1:
            othercounter+=1
        toggle = 0
        image = load_image(f"finished_frameseqs/scream_4/{f}")
        image.save(f"finished_frameseqs/scream_4t/{str(counter).zfill(5)}.png")
    else:
        print("doing replace")
        toggle = 1
        # rmslist.append(rms) #for finding loudest in combination with if(False) above
        image = load_image(f"finished_frameseqs/scream_4text/{othercounter}.png")
        image.save(f"finished_frameseqs/scream_4t/{str(counter).zfill(5)}.png")
    counter += 1

