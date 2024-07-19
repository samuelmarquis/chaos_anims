from .screamproject import *
from parameters import *

number = 0
name = f"{title}"
stem_suf = ['v','p','k','i','b']

flamepath = f"{chaosroot}/0.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    v0 = val_curve(0)
    # Iterator 1:
    iterators[0].offset = thin(pol2car(bflows.rms, vflows.colorwheel), 4)
    # Iterator 2:
    iterators[1].x_axis_angle = thin(gatescaler(iflows.rms), 8)
    iterators[1].y_axis_angle = thin(gatescaler(iflows.rms)+ 90, 8)
    iterators[1].offset = thin(pol2car(bflows.rms, iflows.colorwheel), 4)
    # Iterator 3:
    iterators[2].x_axis_angle = thin(gatescaler(bflows.zcr), 8)
    iterators[2].y_axis_angle = thin(gatescaler(bflows.zcr) + 90, 8)
    iterators[2].ngon = iflows.noteC
    iterators[2].ngon_power = kflows.rms
    iterators[2].offset = thin(pol2car(bflows.rms, iflows.colorwheel), 4)