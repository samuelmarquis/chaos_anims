from PIL import Image
import numpy as np
from numpy import random

hist = np.zeros((512,512), np.uint8)

f0 = lambda x,y:(x/2,y/2)
f1 = lambda x,y:((x+1)/2,y/2)
f2 = lambda x,y:(x/2,(y+1)/2)
flist = [f0,f1,f2]
x = random.rand() * 2 - 1
y = random.rand() * 2 - 1

iteration_depth = 0
while iteration_depth < 1000000:
    iteration_depth += 1
    i = random.randint(0,3)
    if iteration_depth % 1000 == 0:
        print(f"{iteration_depth}...")
    x,y = flist[i](x,y)
    if iteration_depth < 20:
        continue
    scaled_x = int((x/2+0.5)*512)
    scaled_y = int((y/2+0.5)*512)
    #print(f"{scaled_x},{scaled_y}")
    if scaled_x < 0 or scaled_x > 512 or scaled_y < 0 or scaled_y > 512:
        #print("skip")
        continue
    hist[scaled_x, scaled_y] += 1


im = Image.fromarray(hist, mode="L")
im.save('hist.png')