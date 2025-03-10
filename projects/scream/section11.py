from .screamproject import *
from parameters import *

number = 11
stem_suf = ['v','k','c','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    kflows = sflows["k"]
    cflows = sflows["c"]
    bflows = sflows["b"]

    # Camera:
    # Iterator 6:
    iterators[1].pre_blur = kflows.rms
    # Iterator 2:
    iterators[2].x_axis_angle = bflows.zcr * 360
    iterators[2].x_axis_length = bflows.rms * 4
    iterators[2].y_axis_angle = vflows.zcr * 360
    iterators[2].y_axis_length = flows.lf * 4
    # Iterator 3:
    iterators[3].arcsech = cflows.rms
    # Iterator 4:
    iterators[4].vibration2_dm = cflows.rms * 80
    iterators[4].vibration2_dmfreq = vflows.zcr * 15
    iterators[4].vibration2_tm = flows.bandwidth * 80
    iterators[4].vibration2_tmfreq = flows.centroid * 10
    iterators[4].vibration2_fm2 = bflows.noteC * 5
    iterators[4].vibration2_fmfreq2 = bflows.centroid * 20
    iterators[4].vibration2_am2 = bflows.rolloff * 5
    iterators[4].vibration2_amfreq2 = bflows.flux * 20

