from .screamproject import *
from parameters import *

number = 1
stem_suf = ['k']

flamepath = f"{chaosroot}/{number}.chaos"
# palate locations: 0,.4, and then 0-1 for the other 2
# it2 xlen/ylen deviate slightly around 1
# it1 offset stay in (0, 0) to (0.25,-0.25)
#blur between 0.1 and 0.001
def animate(iterators, flows, sflows):

    kflows = sflows["k"]

    v0 = ValCurve(0)
    # Camera:
    # Iterator 1:
    # Iterator 2:
    iterators[2].x_axis_angle =  gatescaler(kflows.rms, isangle=True)
    iterators[2].x_axis_length = flows.lm*2 + 0.2
    # Iterator 3:
    iterators[3].x_axis_length = ((flows.colorwheel ** 0.1) * 2 - 1) + 0.1
    iterators[3].palette_index = flows.rms ** 1.2
    # Iterator 4:
    iterators[4].palette_index = kflows.rms
    # Iterator 5:
    iterators[5].y_axis_angle = gatescaler(flows.lf, isangle=True)
    iterators[5].y_axis_length = flows.hm*2 + 0.2
    iterators[5].palette_index =  flows.lf ** 1.2