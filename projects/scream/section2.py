from .screamproject import *
from parameters import *

number = 2
stem_suf = ['v','p','k','i','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    # Iterator 1:
    iterators[0].offset = (bflows.rms *2 - 1, bflows.colorwheel * 2 - 1)
    # Iterator 2:
    iterators[1].modulus_x = (slew(kflows.lf, 0.05, "down") * 3) ** 0.5
    iterators[1].modulus_y = (slew(pflows.lm, 0.05, "down") * 3) ** 0.5
    iterators[1].offset = (bflows.lm*2-1, bflows.hm*2-1)
    # Iterator 3:
    iterators[2].vibration2_freq = bflows.mincorr * 100
    iterators[2].vibration2_freq2 = bflows.majcorr * 100
    iterators[2].vibration2_dmfreq = bflows.noteC * 50
    iterators[2].vibration2_tmfreq = bflows.noteG * 75
    iterators[2].vibration2_fmfreq2 = bflows.noteEb * 125
    iterators[2].vibration2_amfreq2 = bflows.noteAb * 200

