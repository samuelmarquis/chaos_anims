from .screamproject import *
from parameters import *

number = 1
stem_suf = ['v','p','k','i','b']

flamepath = f"{chaosroot}/{number}.chaos"
# it2 powx/powy deviate slightly around 1
# it2 xlen/ylen deviate slightly around 1
# it1 offset stay in (0, 0) to (0.25,-0.25)
#blur between 0.1 and 0.001
def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]
    v0 = val_curve(0)
    # Iterator 1:
    iterators[0].offset = pol2car(kflows.rms, vflows.colorwheel)
    # Iterator 2:
    iterators[1].x_axis_length = flows.lf * 0.2 + 0.9
    iterators[1].y_axis_length = flows.lf * 0.2 + 0.9
    iterators[1].linearT_powX = bflows.rms * 0.2 + 0.9
    iterators[1].linearT_powY = bflows.rms * 0.2 + 0.9
    # Iterator 3:
    iterators[2].pre_blur = (iflows.majcorr * 0.1) ** 2
    # Iterator 4:
    iterators[3].Base_weight = iflows.rms ** 4