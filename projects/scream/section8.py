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
    # Camera:
    # Iterator 1:
    # Iterator 2:
    iterators[2].faber_x_hypergon = bflows.rms
    iterators[2].faber_x_hypergon_r = bflows.colorwheel
    iterators[2].faber_x_star = flows.centroid
    iterators[2].faber_x_lituus = -2 + (kflows.rms*2)
    iterators[2].faber_x_lituus_a = vflows.colorwheel * 8 - 4
    iterators[2].faber_x_super = pflows.rms
    # Iterator 3:
    # Iterator 4:

