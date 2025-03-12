from .screamproject import *
from parameters import *

number = 5
stem_suf = ['p','k','v','b']

flamepath = f"{chaosroot}/{number}.chaos"
#spndist < 0.2
def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    #iflows = sflows["i"]
    bflows = sflows["b"]
    # Camera:
    iterators[0].blocky_mp = (8 - kflows.rms*8) + (4-vflows.rms * 4)
    # Iterator 1:
    iterators[1].checks_x = pflows.rms
    iterators[1].checks_y = -pflows.hf + 1
    iterators[1].checks_size = bflows.lm
    iterators[1].checks_rnd = bflows.hm
    iterators[1].offset = pol2car(1 - bflows.rms, bflows.colorwheel)
    # Iterator 2:
    iterators[2].SphericalN_dist = kflows.lf
    # Iterator 3:
    iterators[3].vibration2_dm = kflows.lf * 2
    iterators[3].vibration2_dmfreq = vflows.colorwheel * 50
    iterators[3].vibration2_fm = pflows.rms * 5
    iterators[3].vibration2_fmfreq = vflows.rms * 50
    iterators[3].vibration2_am = pflows.lm * 4
    iterators[3].vibration2_amfreq = kflows.rms * 10
    iterators[3].vibration2_tm2 = bflows.rms * 2
    iterators[3].vibration2_tmfreq2 = bflows.colorwheel * 10
    iterators[3].vibration2_fm2 = vflows.centroid * 5
    iterators[3].vibration2_fmfreq2 = bflows.majcorr * 100
