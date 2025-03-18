from .screamproject import *
from parameters import *

number = 910
stem_suf = ['p','k','v','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):

    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    bflows = sflows["b"]
    # Camera:
    # Iterator 1:
    iterators[1].ngon = pflows.rms ** 0.01
    iterators[1].ngon_power = 1 - kflows.rms
    # Iterator 2:
    # Iterator 3:
    iterators[3].x_axis_angle = gatescaler(vflows.rms*2, 0.5, True) * 360
    iterators[3].y_axis_angle = gatescaler(vflows.rms*2, 0.5, True) * 360 + 90
    iterators[3].offset = pol2car(bflows.rms, bflows.colorwheel)
    # Iterator 4:
    iterators[4].x_axis_length = 1 - flows.rms
    iterators[4].y_axis_length = 1 - flows.rms
    iterators[4].escher_beta = gatescaler(kflows.rms * 40)