from scipy import signal
import numpy as np
from math import tau
from numpy.random import default_rng
from scipy.interpolate import PchipInterpolator
from .core import val_curve, flow_size

def pol2car(rho, phi):
    rho = rho.value
    phi = phi.value
    x = rho * np.cos(phi*tau)
    y = rho * np.sin(phi*tau)
    return val_curve(x, y)

def lti(values):
    return signal.lti(values)

def alternating_mask(points, hv=1):
    global flow_size
    r = np.zeros(flow_size)
    n = hv
    for p in points:
        r[p:] = n
        n ^= hv
    return val_curve(r)

def slew(values, rate, direction = 'both'): #direction can be 'up', 'down', or 'both'
    newval = values
    if direction == 'up':
        for i in range(len(values) - 1):
            if abs(values[i + 1] - values[i]) > rate and values[i+1] > values[i]:
                newval[i + 1] = values[i] + rate
        return newval
    if direction == 'down':
        for i in range(len(values) - 1):
            if abs(values[i + 1] - values[i]) > rate and values[i + 1] < values[i]:
                newval[i + 1] = values[i] - rate
        return newval
    if direction == 'both':
        for i in range(len(values) - 1):
            if abs(values[i + 1] - values[i]) > rate:
                newval[i + 1] = values[i] + (rate * (-1 if values[i] > values[i+1] else 1))
        return newval

def iron(values, thresh=0.1):
    r = values
    for i in range(1,len(values)):
        if abs(r[i-1]-values[i]) > thresh:
            r[i] = values[i]
        else:
            r[i] = r[i-1]
    return r

def flat_thin(vc, thresh=0.01, n=5):
    v, v2, k, bt, ft = vc.unpack()
    index = [0]
    r = v[0]
    for i in range(1, len(v)):
        if abs(r-v[i]) > thresh:
            if index[-1] != i-1:
                index.append(i-1)
            index.append(i)
            r = v[i]
    if v2 is not None:
        v2 = v2[index]
    return val_curve(v[index],v2,k[index],bt[index],ft[index])

def flat_time(vc, n = 5, thresh=0.01):
    v, v2, k, bt, ft = vc.unpack()
    index = [0]
    r = v[0]
    sc = 0
    for i in range(1, len(v)):
        if sc > 0:
            sc -= 1
            continue
        if abs(r - v[i]) > thresh:
            for j in range(n):
                if abs(r - v[i+j]) < thresh:
                    sc = j
                    break
            else:
                if index[-1] != i - 1:
                    index.append(i - 1)
                index.append(i)
                r = v[i]
    if v2 is not None:
        v2 = v2[index]
    return val_curve(v[index], v2, k[index], bt[index], ft[index])



def thin(vc, factor):
    flow_size = len(vc.value)
    tfactor = sorted(default_rng().choice(range(flow_size), flow_size//factor, replace=False))
    values2 = None
    if vc.value2 is not None:
        values2 = vc.value2[tfactor]
    return val_curve(vc.value[tfactor], values2, vc.knots[tfactor], vc.bten[tfactor], vc.ften[tfactor])

def bound(values, high=1, low=0):
    return values.clip(min=low, max=high)

def sinusoidal(values, high=1, low=0):
    return np.sin((values * np.pi / len(values)) + (3*np.pi / 2))

def gatescaler(values, thresh=0.5, isangle=False): #NOT BOUNDED ON [0,1] USE ONLY FOR ROTATION AND PARAMETERS THAT CAN BECOME ARBITRARILY LARGE
    output = np.zeros(len(values))
    v = 0.5
    for n in range(len(values)):
        if values[n] > thresh or thresh == 0:
            v += values[n]-thresh
        output[n] = v
    return output if isangle==False else angle(output)

def jitter(values = None, lr=0, hr=1, vs=None):
    global flow_size
    r = np.random.random(flow_size)
    r *= (hr-lr)
    r += (lr)
    if vs is not None:
        r *= vs
    if values is not None:
        return values + r
    else:
        return r

def angle(values):
    return values % 360