from ...parameters import *


#title = "mbf"
number = 4
name = f"{title}_{number}"
#name = title
stemprefixes = []
#stemprefixes = []
#audiopath = f"audio/{project}/{name}.wav"
audiopath = f"audio/mbf.wav"
#flamepath = f"chaos/{name}.chaos"
flamepath = f"chaos/example.chaos"
def animate(automators, flows):
    automators[1].xangle = flows.rms * 360
    automators[1].yangle = thinify(flows.rms * 360 + 90, 4)
    automators[2].julian2_power = flows.colorwheel * 2
    automators[2].Iterator_1_weight = flows.colorwheel * 8
    x, y = pol2car(flows.rms, flows.colorwheel)

    automators[0].offset = thinify((x, y), 16)