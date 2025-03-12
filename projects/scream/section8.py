import math

from .screamproject import *
from parameters import *

number = 8
stem_suf = ['p','k','i','v','b']

flamepath = f"{chaosroot}/{number}.chaos"

#separation 0.01-2
#separation_inside 0-1
def animate(iterators, flows, sflows):

    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]

    # Camera:
    # Iterator 1:
    # Iterator 2:
    # Iterator 3:
    iterators[3].x_axis_angle = 360*vflows.colorwheel
    iterators[3].y_axis_angle = 360*vflows.colorwheel + 90
    iterators[3].offset = pol2car(pflows.rms, bflows.colorwheel)
    # Iterator 4:
    iterators[4].vibration2_dir = bflows.colorwheel * math.pi
    iterators[4].vibration2_angle = bflows.colorwheel * math.pi
    iterators[4].vibration2_dir2 = vflows.colorwheel * math.pi
    iterators[4].vibration2_angle2 = vflows.colorwheel * math.pi
    iterators[4].vibration2_dm = bflows.rms * 2
    iterators[4].vibration2_dmfreq = bflows.centroid * 10
    iterators[4].vibration2_am = kflows.rms * 4
    iterators[4].vibration2_amfreq = bflows.lf * 10
    iterators[4].vibration2_tm2 = iflows.rms * 10
    iterators[4].vibration2_tmfreq2 = vflows.colorwheel * 20
    iterators[4].vibration2_fm2 = pflows.rms * 5
    iterators[4].vibration2_fmfreq2 = bflows.rms * 10