from .screamproject import *
from parameters import *

number = 7
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
    iterators[0].pr_A = lin() * 4
    iterators[0].pr_B = lin() * pflows.rms * 2
    iterators[0].pr_A1 = 3 - slew(kflows.rms, 0.08, 'down')*2
    iterators[0].pr_B1 = bflows.rms
    iterators[0].pr_A2 = iflows.rms
    iterators[0].pr_B2 = 1 - kflows.rms

    iterators[0].x_axis_angle = flat_time(gatescaler(kflows.rms*100, 0, True))
    iterators[0].x_axis_length = 1-pflows.rms ** 10
    iterators[0].y_axis_angle = flat_time(gatescaler(kflows.rms*100, 0, True) + 90)
    iterators[0].y_axis_length = 1-pflows.rms ** 10

    iterators[3].x_axis_angle = vflows.colorwheel * 360
    iterators[3].y_axis_angle = vflows.colorwheel * 360 + 90
    iterators[3].separation_x = 2 - pflows.rms
    iterators[3].separation_y = 2 - pflows.hm
    iterators[3].separation_xinside = kflows.rms
    iterators[3].separation_yinside = kflows.lf
    iterators[3].offset = pol2car(iflows.rms, bflows.colorwheel)
    # Iterator 4:
