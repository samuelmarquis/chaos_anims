import os
import xml.etree.ElementTree as ET
import itertools
import numpy as np
import sys
import matplotlib.pyplot as plt
np.set_printoptions(threshold=sys.maxsize)

def visualize_audio_flows(audio_path):
    audio_data, sr, frame_length, duration_f, duration_s = load_song(audio_path)
    flows = compute_flows(audio_data, sr)

    # Plot
    fig, axs = plt.subplots(3, 1, figsize=(12, 6))

    axs[0].plot(flows.rms.value)
    axs[0].set_ylabel('RMS (normalized)')

    axs[1].plot(flows.colorwheel.value)
    axs[1].set_ylabel('Color Wheel')

    axs[2].plot(flows.centroid.value)
    axs[2].set_ylabel('Spectral Centroid (normalized)')

    for ax in axs:
        ax.set_xlabel('Time (s)')

    plt.tight_layout()
    plt.show()

from projects.truce.section1 import *

visualize_audio_flows(audiopath)

exit(0)

song, sr, _, duration_f, duration_s = load_song(audiopath)
flows = compute_flows(song, sr)
print(f"{flows.rms.value.shape}, {np.mean(flows.colorwheel.value)}")



stems = []
sflows = {}
for s in stemnames:
    sflows[s] = compute_flows(load_song(f"{audioroot}/{s}.wav", stem=True)[0], sr)
    print(f" - Computed flows for stem: {s}")

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

flame.write('chaos/new.chaos')
print("Successfully wrote chaos/new.chaos. Exiting")
