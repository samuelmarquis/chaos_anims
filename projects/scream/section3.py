from .screamproject import *
from parameters import *

number = 3
stem_suf = ['v','p','k','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    bflows = sflows["b"]
    # Iterator 1:
    iterators[1].x_axis_angle = vflows.colorwheel * 360
    iterators[1].y_axis_angle = vflows.colorwheel * 360 + 90
    iterators[1].offset = pol2car(slew(kflows.rms, 0.05, "down"), flows.colorwheel)
    # Iterator 2:
    iterators[2].vibration2_tm = bflows.rms * 5
    iterators[2].vibration2_tmfreq = bflows.noteAb
    # Iterator 3:
    iterators[3].x_axis_angle = bflows.colorwheel * 360
    iterators[3].x_axis_length = bflows.noteEb * 4 + 0.2
    iterators[3].y_axis_angle = bflows.colorwheel * 360 + 90
    iterators[3].y_axis_length = bflows.noteEb * 4 + 0.2
