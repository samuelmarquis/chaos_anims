from .truce_project import project_name, title, audioroot, chaosroot
from parameters import *

number = 1
name = f"{number}"
stemnames = [f"{name}v"]
audiopath = f"{audioroot}/{name}.wav"
flamepath = f"{chaosroot}/1.chaos"

def animate(iterators, flows, sflows):
    vflows = sflows["1v"]
    # Iterator 1:
    iterators[0].vibration2_fmfreq = flat_time(vflows.colorwheel)
    iterators[0].vibration2_amfreq = vflows.colorwheel
    iterators[0].vibration2_tm2 = thin(vflows.colorwheel, 2)
    iterators[0].vibration2_tmfreq2 = thin(vflows.colorwheel, 2)
    iterators[0].vibration2_amfreq2 = thin(vflows.colorwheel, 2)
    iterators[0].offset = thin(pol2car(vflows.rms, vflows.colorwheel), 2)
    # Iterator 2:
    iterators[1].offset = thin(pol2car(vflows.rms, vflows.colorwheel*0.25), 2)
    # Iterator 3:
    iterators[2].offset = thin(pol2car(vflows.rms, vflows.colorwheel*0.5), 2)
    # Iterator 4:
    iterators[3].offset = thin(pol2car(vflows.rms, vflows.colorwheel*0.75), 2)
    # Iterator 5:
    iterators[4].x_axis_angle = thin(vflows.colorwheel, 2)
    iterators[4].x_axis_length = thin(vflows.colorwheel, 2)
    iterators[4].y_axis_angle = thin(vflows.colorwheel, 2)
    iterators[4].y_axis_length = thin(vflows.colorwheel, 2)
    iterators[4].offset = thin(pol2car(vflows.rms, vflows.colorwheel*0.75), 2)
