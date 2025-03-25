from .screamproject import *
from parameters import *

number = 8
stem_suf = ['c','k','b', 'v']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):

    pflows = sflows["c"]
    kflows = sflows["k"]
    bflows = sflows["b"]
    vflows = sflows['v']
    # Iterator 1:
    iterators[1].offset = (bflows.rms *2 - 1, bflows.colorwheel * 2 - 1)
    # Iterator 2:
    iterators[2].modulus_x = (slew(kflows.lf, 0.05, "down") * 3) ** 0.5
    iterators[2].modulus_y = (slew(pflows.lm, 0.05, "down") * 3) ** 0.5
    iterators[2].offset = (bflows.lm*2-1, bflows.hm*2-1)
    # Iterator 3:
    iterators[3].vibration2_freq = bflows.mincorr * 100
    iterators[3].vibration2_freq2 = bflows.majcorr * 100
    iterators[3].vibration2_dmfreq = vflows.noteC * 50
    iterators[3].vibration2_tmfreq = vflows.noteF * 75
    iterators[3].vibration2_fmfreq2 = vflows.noteGb * 125
    iterators[3].vibration2_amfreq2 = vflows.noteDb * 200

