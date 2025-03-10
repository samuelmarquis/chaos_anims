import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2

from torchvision import transforms
#from transformers import AutoModelForImageSegmentation
from util import sorted_alphanumeric, change_contrast
import warnings
#from segment_anything import SamPredictor, sam_model_registry, SamAutomaticMaskGenerator
import hydra
from sam2.build_sam import build_sam2_video_predictor

mask_colors = [[255,255,255],
                   [255,0,0],[0,255,0],[0,0,255],
                   [255,255,0],[255,0,255],[0,255,255],
                   [255,127,0],[255,0,127],[127,255,0],[0,255,127],[127,0,255],[0,127,255],
                   [255,127,127],[127,255,127],[127,127,255],
                   [127,0,0],[0,127,0],[0,0,127],[127,127,0],[127,0,127],[0,127,127]]

warnings.filterwarnings('ignore')
"""
def segment_bw(source_dir, target_dir, size):
    model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
    torch.set_float32_matmul_precision(['high', 'highest'][0])
    model.to('cuda')
    model.eval()

    # Data settings
    image_size = (size, size)
    transform_image = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    n = 0
    for f in sorted_alphanumeric(os.listdir(source_dir)):
        image = Image.open(f"{source_dir}/{f}")

        input_images = transform_image(image).unsqueeze(0).to('cuda')

        # Prediction
        with torch.no_grad():
            preds = model(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)

        a0 = np.array(change_contrast(image, 100))
        a1 = np.array(mask)
        b = np.repeat(a1[:, :, np.newaxis], 3, axis=2)
        a2 = np.bitwise_and(a0, a1[..., None])
        ""
        lb = np.array([0, 0, 0])
        lmb = np.array([40, 40, 40])
        umb = np.array([80, 80, 80])
        ub = np.array([255, 255, 255])

        mask1 = np.all((a2 < lmb), axis=2)
        mask2 = np.all((a2 >= lmb) & (a2 <= umb), axis=2)
        mask3 = np.all((a2 > umb), axis=2)

        a2[mask1] = [255, 0, 0]
        a2[mask2] = [0, 255, 0]
        a2[mask3] = [0, 0, 255]
        ""

        Image.fromarray(a1).save(f"{target_dir}/{f}")

        #mask.save(f"{target_dir}/{f}")
        n += 1
        if n % 100 == 0 and n > 0:
            print(f" - segmented {n} source images")
"""

"""
def segment_anything(source_dir, target_dir, size):
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    mask_colors = [[255,255,255],
                   [255,0,0],[0,255,0],[0,0,255],
                   [255,255,0],[255,0,255],[0,255,255],
                   [255,127,0],[255,0,127],[127,255,0],[0,255,127],[127,0,255],[0,127,255],
                   [255,127,127],[127,255,127],[127,127,255],
                   [127,0,0],[0,127,0],[0,0,127],[127,127,0],[127,0,127],[0,127,127]]
    sam = sam_model_registry["vit_b"](checkpoint="models/sam_checkpoints/ViT_B.pth").to(device=DEVICE) # Smallest model
#   sam = sam_model_registry["vit_l"](checkpoint="models/sam_checkpoints/ViT_L.pth").to(device=DEVICE)  # Medium model
#   sam = sam_model_registry["vit_h"](checkpoint="models/sam_checkpoints/ViT_H.pth").to(device=DEVICE) # Largest model

    mask_generator = SamAutomaticMaskGenerator(sam)

    for n, f in enumerate(sorted_alphanumeric(os.listdir(source_dir))):

        image = Image.open(f"{source_dir}/{f}")
        a0 = np.array(image.convert("RGB"))
        masklist = mask_generator.generate(a0)
        for c,mask in enumerate(masklist):
            if c >= len(mask_colors):
                break
            #print(mask['segmentation'].shape)
            a0[mask['segmentation']] = mask_colors[c]
        Image.fromarray(a0).save(f"{target_dir}/{f}")
        if n % 10 == 0 and n > 0:
            print(f" - segmented {n} source images")
"""
def segment_anything(source_dir, target_dir, size):
    checkpoint = "sam2/checkpoints/sam2.1_hiera_tiny.pt"
    model_cfg = "configs/sam2.1/sam2.1_hiera_t.yaml"

    predictor = build_sam2_video_predictor(model_cfg, checkpoint)

    def show_mask(mask, ax, obj_id=None, random_color=False, show=True):
        if random_color:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
        else:
            cmap = plt.get_cmap("tab10")
            cmap_idx = 0 if obj_id is None else obj_id
            color = np.array([*cmap(cmap_idx)[:3], 0.6])
        h, w = mask.shape[-2:]

        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)

        if show:
            ax.imshow(mask_image)
        return mask_image

    def show_points(coords, labels, ax, marker_size=200):
        pos_points = coords[labels == 1]
        neg_points = coords[labels == 0]
        ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white',
                   linewidth=1.25)
        ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white',
                   linewidth=1.25)

    def show_box(box, ax):
        x0, y0 = box[0], box[1]
        w, h = box[2] - box[0], box[3] - box[1]
        ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))

    def add_obj(frame, id, points, labels):
        points = np.array(points, dtype=np.float32)
        labels = np.array(labels, np.int32)
        return predictor.add_new_points_or_box(
            inference_state=state,
            frame_idx=frame,
            obj_id=id,
            points=points,
            labels=labels,
        )


    # scan all the JPEG frame names in this directory
    frame_names = [
        p for p in os.listdir(source_dir)
        if os.path.splitext(p)[-1] in [".jpg"]
    ]
    frame_names.sort(key=lambda p: int(os.path.splitext(p)[0]))
    # take a look the first video frame
    frame_idx = 20
    plt.figure(figsize=(9, 9))
    plt.title(f"frame {frame_idx}")
    plt.imshow(Image.open(os.path.join(source_dir, frame_names[frame_idx])))

    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
        state = predictor.init_state(video_path=source_dir)

        frame=20
        print("Creating masks")
        add_obj(20,1,[[288,344], [445,317], [350,333], [307,348]], [1,1,0,0])
        add_obj(20, 2, [[350,313], [343,358],[365,359],[325,432],[322,350]], [1, 1, 1,1,1])
        add_obj(20, 3, [[367,251], [361,162],[386,122]], [1, 1, 0])
        add_obj(20, 4, [[383,123]], [1])
        add_obj(20, 5, [[313,86]], [1])
        _, out_obj_ids, out_mask_logits = add_obj(20, 6, [[160,400]], [1])


        confirm = True
        if confirm:
            # show the results on the current (interacted) frame
            plt.figure(figsize=(9, 9))
            plt.title(f"frame {20}")
            plt.imshow(Image.open(os.path.join(source_dir, frame_names[frame])))
            #show_points(points, labels, plt.gca())
            show_mask((out_mask_logits[0] > 0.0).cpu().numpy(), plt.gca(), obj_id=out_obj_ids[0])
            show_mask((out_mask_logits[1] > 0.0).cpu().numpy(), plt.gca(), obj_id=out_obj_ids[1])
            show_mask((out_mask_logits[2] > 0.0).cpu().numpy(), plt.gca(), obj_id=out_obj_ids[2])
            show_mask((out_mask_logits[3] > 0.0).cpu().numpy(), plt.gca(), obj_id=out_obj_ids[3])
            show_mask((out_mask_logits[4] > 0.0).cpu().numpy(), plt.gca(), obj_id=out_obj_ids[4])
            show_mask((out_mask_logits[5] > 0.0).cpu().numpy(), plt.gca(), obj_id=out_obj_ids[5])
            plt.show()

        print("Sending it")

        # run propagation throughout the video and collect the results in a dict
        video_segments = {}  # video_segments contains the per-frame segmentation results
        for out_frame_idx, out_obj_ids, out_mask_logits in predictor.propagate_in_video(state):
            torch.cuda.empty_cache()
            video_segments[out_frame_idx] = {
                out_obj_id: (out_mask_logits[i] > 0.0).cpu().numpy()
                for i, out_obj_id in enumerate(out_obj_ids)
            }
            a = np.array(Image.open(os.path.join(source_dir, frame_names[out_frame_idx])).convert("RGB"))
            for out_obj_id, out_mask in video_segments[out_frame_idx].items():
                reshaped = out_mask.reshape(size,size)
                a[reshaped] = mask_colors[out_obj_id]

            res = cv2.resize(a, dsize=(1024,1024), interpolation=cv2.INTER_CUBIC)
            Image.fromarray(res).save(f"{target_dir}/patch/{out_frame_idx:05d}.png")

"""        # render the segmentation results every few frames

        for out_frame_idx in range(0, len(frame_names)):
            a = np.array(Image.open(os.path.join(source_dir, frame_names[out_frame_idx])).convert("RGB"))
            for out_obj_id, out_mask in video_segments[out_frame_idx].items():
                a[out_mask] = mask_colors[out_mask]

            Image.fromarray(a).save(f"{target_dir}/{out_frame_idx:05d}.png")"""

if __name__ == '__main__':
    segment_anything("vid_pipe/scream11/src_frames", "vid_pipe/scream11/masks",512)