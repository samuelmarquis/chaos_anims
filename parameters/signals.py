from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
from math import tau
from numpy.random import default_rng
from scipy.interpolate import PchipInterpolator
from .core import val_curve

def read_flow_size():
    with open("flow.dat", "r") as f:
        return int(f.readline())

def pol2car(rho, phi):
    rho = rho.value
    phi = phi.value
    x = rho * np.cos(phi*tau)
    y = rho * np.sin(phi*tau)
    return val_curve(x, y)

def lti(values):
    return signal.lti(values)

def alternating_mask(points, hv=1):
    flow_size = read_flow_size()
    r = np.zeros(flow_size)
    n = hv
    for p in points:
        r[p:] = n
        n ^= hv
    return val_curve(r)

def lin():
    flow_size = read_flow_size()
    return val_curve(np.linspace(0, 1, flow_size))

def slew(vc, rate, direction = 'both'): #direction can be 'up', 'down', or 'both'
    values, v2, k, bt, ft = vc.unpack()
    newval = values
    if direction == 'up':
        for i in range(len(values) - 1):
            if abs(values[i + 1] - values[i]) > rate and values[i+1] > values[i]:
                newval[i + 1] = values[i] + rate

    if direction == 'down':
        for i in range(len(values) - 1):
            if abs(values[i + 1] - values[i]) > rate and values[i + 1] < values[i]:
                newval[i + 1] = values[i] - rate

    if direction == 'both':
        for i in range(len(values) - 1):
            if abs(values[i + 1] - values[i]) > rate:
                newval[i + 1] = values[i] + (rate * (-1 if values[i] > values[i+1] else 1))

    return val_curve(newval, v2, k, bt, ft)

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
    for i in range(1, len(v)-n):
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
    return val_curve(output if isangle==False else angle(output))

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

def visualize_audio_flows(audio_path):
    print("broken")
    exit(1)
    # Plot
    fig, axs = plt.subplots(3, 1, figsize=(12, 6))

    axs[0].plot(flows.rms.value)
    axs[0].set_ylabel('RMS (normalized)')

    axs[1].plot(flows.colorwheel.value)
    axs[1].set_ylabel('Color Wheel')

    axs[2].plot(flows.centroid.value)
    axs[2].set_ylabel('Spectral Centroid (normalized)')

    for ax in axs:
        ax.set_xlabel('Time (s)')

    plt.tight_layout()
    plt.show()