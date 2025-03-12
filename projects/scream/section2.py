from .screamproject import *
from parameters import *

number = 2
stem_suf = ['p','k','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):

    pflows = sflows["p"]
    kflows = sflows["k"]

    bflows = sflows["b"]
    # Iterator 1:
    iterators[1].offset = (bflows.rms *2 - 1, bflows.colorwheel * 2 - 1)
    # Iterator 2:
    iterators[2].modulus_x = (slew(kflows.lf, 0.05, "down") * 3) ** 0.5
    iterators[2].modulus_y = (slew(pflows.lm, 0.05, "down") * 3) ** 0.5
    iterators[2].offset = (bflows.lm*2-1, bflows.hm*2-1)
    # Iterator 3:
    iterators[3].vibration2_freq = bflows.mincorr * 100
    iterators[3].vibration2_freq2 = bflows.majcorr * 100
    iterators[3].vibration2_dmfreq = bflows.noteC * 50
    iterators[3].vibration2_tmfreq = bflows.noteG * 75
    iterators[3].vibration2_fmfreq2 = bflows.noteEb * 125
    iterators[3].vibration2_amfreq2 = bflows.noteAb * 200

