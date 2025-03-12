from .screamproject import *
from parameters import *

number = 6
stem_suf = ['p','k','i','v','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    hard1 = alternating_mask([753,778])
    hard2 = alternating_mask([753])
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    # Camera:
    iterators[0].curve_xamp = flat_thin(vflows.noteF *3-1.5, 0.5)
    iterators[0].curve_yamp = flat_thin(vflows.noteEb *3-1.5, 0.5)
    iterators[0].curve_xlength = 1 - (hard1*2)
    iterators[0].curve_ylength = 1 - (hard2*2)
    # Iterator 1:

    iterators[1].x_axis_length = flat_thin(1 - kflows.rms)
    iterators[1].y_axis_angle = flat_thin(bflows.rms * 80 + iflows.rms * 10)
    iterators[1].y_axis_length = flat_thin(1- kflows.rms)
    # Iterator 2:
    iterators[2].x_axis_angle = flat_thin(bflows.rms * 80 + iflows.rms * 10)
    iterators[2].x_axis_length = flat_thin(1- kflows.rms)

    iterators[2].y_axis_length = flat_thin(1- kflows.rms)
    # Iterator 3:
    iterators[3].ngon_sides = flat_thin(iflows.rms * 3 + 2)
    iterators[3].ngon_power = flat_thin(kflows.rms + 1.1)
    iterators[3].ngon_corners = flat_thin(vflows.centroid + 1)
    iterators[3].ngon_circle = flat_thin(bflows.colorwheel + 1)
    # Iterator 4: