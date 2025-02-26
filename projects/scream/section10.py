from .screamproject import *
from parameters import *

number = 10
stem_suf = ['p','k','i','v','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    # Camera:
    # Iterator 1:
    iterators[1].x_axis_angle = vflows.colorwheel * 360
    iterators[1].y_axis_angle = vflows.colorwheel * 360 + 90
    iterators[1].julian_dist = iflows.colorwheel + 1
    iterators[1].offset = pol2car(flows.rms ** 0.1, gatescaler(pflows.rms, 0) * 0.2)
    # Iterator 2:
    iterators[2].juliascope_power = 1 - kflows.rms
    # Iterator 3:
    iterators[3].x_axis_length = 1 + bflows.rms * 0.1
    iterators[3].y_axis_length = 1 + bflows.rms * 0.1