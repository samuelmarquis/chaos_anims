import re

import cv2
import numpy as np
from functools import partial

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def saturate(x, hardness=1, center=0.5):
    a = hardness
    b = hardness * center
    return (np.tanh(a*x - b) + 1) / 2

def channel_saturate(a, h=None, c=None):
    if h is None:
        ha = [1, 1, 1]
    if c is None:
        c = [0.5, 0.5, 0.5]

    r, g, b = a[..., 0], a[..., 1], a[..., 2]

    r_new = (np.tanh(h[0] * (r - c[0])) + 1) / 2
    g_new = (np.tanh(h[1] * (g - c[1])) + 1) / 2
    b_new = (np.tanh(h[2] * (b - c[2])) + 1) / 2

    return np.stack([r_new, g_new, b_new], axis=2)

def grad_map(a, left=None, right=None):
    if left is None:
        left = [0, 0, 0]
    if right is None:
        right = [1, 1, 1]

    left = np.array(left)
    right = np.array(right)

    r,g,b = a[..., 0], a[..., 1], a[..., 2]

    # Convert to grayscale using luminance formula (0.299R + 0.587G + 0.114B)
    gray = 0.299 * r + 0.587 * g + 0.114 * b

    r_new = left[0] + (right[0] - left[0]) * gray
    g_new = left[1] + (right[1] - left[1]) * gray
    b_new = left[2] + (right[2] - left[2]) * gray

    return np.stack([r_new, g_new, b_new], axis=2)

def noise(a, l=0.1, tint=None):
    if tint is None:
        tint = [1,1,1]
    n = (np.random.rand(a.shape[0], a.shape[1], a.shape[2])* tint)*2-1
    return a+n*l

def read_image(path):
    a = cv2.imread(path, cv2.IMREAD_COLOR_RGB)
    if a is None:
        return None
    a = a[..., ::-1].astype(np.float32) / 255.0
    return a

def write_image(path, img):
    #img = np.clip(img[..., ::-1] * 255.0, 0, 255).astype(np.uint8)
    img = (img * 255.0).astype(np.uint8)
    cv2.imwrite(path, img)

def edge_detect(a, sh=4):
    cb = False
    if a.dtype == np.float32:
        cb = True
        a = (a*255.0).astype(np.uint8)
    e = ~(a ^ (np.roll(~a, shift=sh, axis=0) | np.roll(~a, shift=sh, axis=1) | np.roll(~a, shift=-sh, axis=0) | np.roll(~a, shift=-sh, axis=1)))
    if cb:
        return np.clip(e,0,1).astype(np.float32)
    return e

if __name__ == '__main__':
    nn = read_image(f"vid_pipe/scream1/a_src_frames/00015.png")
    nn = noise(nn, 1)
    write_image("test.png", nn)
