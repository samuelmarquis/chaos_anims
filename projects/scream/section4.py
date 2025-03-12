from .screamproject import *
from parameters import *

number = 4
stem_suf = ['p','k','i','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    #vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    # Iterator 1:
    # Iterator 2:
    iterators[1].offset = pol2car(kflows.rms, iflows.colorwheel)
    # Iterator 3:
    iterators[2].Truchet_exponent = iflows.rolloff
    iterators[2].Truchet_seed = gatescaler(iflows.colorwheel)
    # Iterator 4:
    iterators[3].vibration2_amp = pflows.rms * 0.1
    iterators[3].vibration2_fmfreq = bflows.colorwheel * 10
    iterators[3].vibration2_amfreq = bflows.centroid * 3
    iterators[3].vibration2_dmfreq2 = bflows.lm * 5
    iterators[3].vibration2_tmfreq2 = bflows.hf * 10