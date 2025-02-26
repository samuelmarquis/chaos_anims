from .screamproject import *
from parameters import *

number = 0
stem_suf = ['v','p','k','i','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    v0 = ValCurve(0)
    # Iterator 1:
    iterators[0].offset = thin(pol2car(pflows.rms, vflows.colorwheel), 2)
    # Iterator 2:
    iterators[1].x_axis_angle = thin(gatescaler(iflows.rms), 4)
    iterators[1].y_axis_angle = thin(gatescaler(iflows.rms)+ 90, 4)
    iterators[1].offset = thin(pol2car(pflows.rms, iflows.colorwheel), 2)
    # Iterator 3:
    iterators[2].x_axis_angle = thin(gatescaler(bflows.zcr), 4)
    iterators[2].y_axis_angle = thin(gatescaler(bflows.zcr) + 90, 4)
    iterators[2].ngon = pflows.rms
    iterators[2].ngon_power = iflows.rms
    iterators[2].offset = thin(pol2car(pflows.rms, iflows.colorwheel), 2)