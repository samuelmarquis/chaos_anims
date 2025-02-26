from .screamproject import *
from parameters import *

number = 11
stem_suf = ['p','k','i','v','b']

flamepath = f"{chaosroot}/{number}.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["v"]
    pflows = sflows["p"]
    kflows = sflows["k"]
    iflows = sflows["i"]
    bflows = sflows["b"]

    # Iterator 1:
    # iterators[1].offset =#maybe need this maybe don't
    # Iterator 2:

    iterators[2].juliascope_power = bflows.centroid

    iterators[2].foci_p_c1 = 1+(vflows.rms * 3)
    iterators[2].foci_p_c2 = 1+(vflows.colorwheel * vflows.centroid * 2.5)
    #iterators[2].palette_index =
    #iterators[2].offset =
    # Iterator 3:
    #iterators[3].x_axis_length =
    #iterators[3].y_axis_length =

    # Iterator 4:
    iterators[4].pre_blur = flows.rms
