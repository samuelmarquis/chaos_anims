from .screamproject import *
from parameters import *

number = 3
stem_suf = ['v','p','k','i','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    # Iterator 1:
    iterators[0].x_axis_angle = vflows.colorwheel * 360
    iterators[0].y_axis_angle = vflows.colorwheel * 360 + 90
    iterators[0].offset = pol2car(slew(kflows.rms, 0.05, "down"), iflows.colorwheel)
    # Iterator 2:
    iterators[1].vibration2_tm = bflows.rms * 5
    iterators[1].vibration2_tmfreq = bflows.noteAb
    # Iterator 3:
    iterators[2].x_axis_angle = bflows.colorwheel * 360
    iterators[2].x_axis_length = bflows.noteEb * 4 + 0.2
    iterators[2].y_axis_angle = bflows.colorwheel * 360 + 90
    iterators[2].y_axis_length = bflows.noteEb * 4 + 0.2
