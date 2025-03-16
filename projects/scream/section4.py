from .screamproject import *
from parameters import *

number = 4
stem_suf = ['p','k','c','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    #vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["c"]
    bflows = sflows["b"]
    # Iterator 1:
    # Iterator 2:
    iterators[2].offset = pol2car(kflows.rms, flows.colorwheel)
    # Iterator 3:
    iterators[3].Truchet_exponent = flows.rolloff
    iterators[3].Truchet_seed = gatescaler(flows.colorwheel)
    # Iterator 4:
    iterators[4].vibration2_amp = pflows.rms * 0.1
    iterators[4].vibration2_fmfreq = bflows.colorwheel * 10
    iterators[4].vibration2_amfreq = bflows.centroid * 3
    iterators[4].vibration2_dmfreq2 = bflows.lm * 5
    iterators[4].vibration2_tmfreq2 = bflows.hf * 10