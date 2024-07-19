import os
import xml.etree.ElementTree as ET
import itertools
import numpy as np
import sys
import matplotlib.pyplot as plt
np.set_printoptions(threshold=sys.maxsize)

from projects.scream.section0 import *

audio_name = f"{name}_{number}"

song, sr, _, duration_f, duration_s = load_song(f"{audioroot}/{audio_name}.wav")
flows = compute_flows(song, sr)
print(f"Computed flows for {audio_name}")

stems = []
sflows = {}
for s in stem_suf:
    sflows[s] = compute_flows(load_song(f"{audioroot}/{audio_name}{s}.wav", stem=True)[0], sr)
    print(f" - Computed flows for stem: {audio_name}{s}")

print("Finished computing stem-flows.")

# GET FRACTAL FLAME
flame = ET.parse(flamepath)
root = flame.getroot()
parent_map = {c: p for p in root.iter() for c in p}
iteratorsparent = root[1].find("node") #iterators. 1 is hardcoded bc format version is 0
assert(iteratorsparent.get("name") == "iterators")
paramlist = []
# FIND ANIMATION POINTS
for child in iteratorsparent.findall('iterator'):
    print(f"# {child.get('name')}:")
    paramlist.append({})
    for curve in itertools.chain(child.iter('curve'), child.iter('vec2_curve')):
        if (curve.get('name') == 'val_curve'):
            x = parent_map[curve].get('name')
            x = x.replace(" ", "_")
            paramlist[-1][x] = curve
            print(f"iterators[{len(paramlist)-1}].{x} = ")
            
iterators = [iterator(param) for param in paramlist]

animate(iterators, flows, sflows)

flame.write(f"chaos/{name}/new.chaos")

print(f"Successfully wrote chaos/{name}/new.chaos. Exiting")
