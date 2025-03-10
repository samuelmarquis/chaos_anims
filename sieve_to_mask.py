import os

import cv2
import numpy as np

#sky
#snow
#jacket
#shirt
#skin
#hair
mask_colors = np.array([[255,255,255],
               [255,255,255],[0,255,255],[0,0,255],
               [255,255,0],[0,0,255],[0,255,0],
               [255,127,0],[255,0,127],[127,255,0],[0,255,127],[127,0,255],[0,127,255],
               [255,127,127],[127,255,127],[127,127,255],
               [127,0,0],[0,127,0],[0,0,127],[127,127,0],[127,0,127],[0,127,127]], dtype=np.uint8)

mask_colors = np.flip(mask_colors.astype(np.float32) / 255.0, axis=1)


def flatten_masks(src_dir, mask_dir, target_dir, n_layers):
    #print(mask_colors.shape)
    for n,f in enumerate(os.listdir(src_dir)):
        #a = np.ndarray(shape=(1024, 1024, 3), dtype=np.float32)
        a = cv2.imread(os.path.join(src_dir, f), cv2.IMREAD_COLOR_RGB).astype(np.float32) / 255.0
        for _m in range(n_layers):
            m = _m+1
            cf = cv2.imread(os.path.join(mask_dir, f"confidences_{n}_{m}.png"), cv2.IMREAD_COLOR_RGB).astype(np.float32) / 255.0
            #print(cf.dtype, a.dtype)

            #cv2.imwrite(os.path.join(target_dir, f"{n:05d}e{m}.png"), cf)

            #Sky
            c = [4,0,4]
            if m==1:
                ca=a*c + [.7,0,.7]
                a = np.where(cf > [0,0,0], ca, a)

            #Snow
            c = [4,0,4]
            if m==2:
                a = np.where(cf > [0,0,0], a*c, a)

            #Jacket
            c = [1,0,0]
            if m==3:
                ca = (a**0.5) * c
                a = np.where(cf > [0.0, 0.0, 0.0], ca, a)

            #Shirt
            c = [1,1,0]
            if m==4:
                a = np.where(cf > [0, 0, 0], c, a)

            #Skin
            c = [0.8,0.7,0.7]
            if m==5:
                ca = (np.tanh(((-a+1) * c + 0.1) * 10 - 6) + 1) / 2
                #ca = a * c
                a = np.where(cf > [0, 0, 0], ca, a)

            #Hair
            c = [0,4,0]
            if m==6:
                a = np.where(cf > [0, 0, 0], a * c, a)

        cv2.imwrite(os.path.join(target_dir, f"{n:05d}.png"), np.minimum(a*255.0, 255, None).astype(np.uint8))

        if n%100==0 and n>0:
            print(f"masked {n} images")


if __name__ == '__main__':
    flatten_masks("vid_pipe/scream11/src_frames", "vid_pipe/scream11/sieve/confidences", "vid_pipe/scream11/masks", 6)