import os
from PIL import Image
from util import sorted_alphanumeric
from video_editor import crop_framesplit
from segment import segment_bw, segment_anything
from fractal_mask import mask
from ebsynth import ebsynth_wrapper
from ffmpeg_wrapper import ffmpeg_wrapper
from os import makedirs

skip_to = 5

pname = "scream"
pidx = 11
#input_vid = "source_video/02.28/IMG_9592.MP4"
style_dir = f"finished_frameseqs/{pname}/{pidx}"

base = "vid_pipe"
name = f"{pname}{pidx}"
pdir = f"{base}/{name}"
audio_name = f"audio/{pname}/{pname}_{pidx}s.wav"
res = 1024

makedirs(f"{pdir}/src_frames", exist_ok=True)
makedirs(f"{pdir}/masks", exist_ok=True)
makedirs(f"{pdir}/style", exist_ok=True)
makedirs(f"{pdir}/style_masks", exist_ok=True)
makedirs(f"{pdir}/output", exist_ok=True)

# STEP 1: src video -> square-cropped frame sequences
#if skip_to <= 1:
#    print("Splitting frames")
#    crop_framesplit(f"{input_vid}", f"{pdir}/src_frames", 512)

# STEP 2: resize style
#if skip_to <= 2:
#    print("Resizing style")
#    for f in sorted_alphanumeric(os.listdir(style_dir)):
#        Image.open(f"{style_dir}/{f}").resize((512,512)).save(f"{pdir}/style/{f}")


# STEP 3: source frames -> source mask
if skip_to <= 3:
    print("Segmenting source")
    segment_anything(f"{pdir}/src_frames", f"{pdir}/masks", 512)

# STEP 4: style frames -> style mask
if skip_to <= 4:
    print("Masking style")
    mask(f"{pdir}/style", f"{pdir}/style_masks", 1024)

# STEP 5: ebsynth :: style frames -> style masks -> source masks -> output frames
if skip_to <= 5:
    print("Running ebsynth")
    ebsynth_wrapper(f"{pdir}/style",
                    f"{pdir}/style_masks",
                    f"{pdir}/masks",
                    f"{pdir}/output")

#n = 0
#for f in sorted_alphanumeric(os.listdir(f"{pdir}/bad_out")):
#    image = Image.open(f"{pdir}/bad_out/{f}").save(f"{pdir}/output/{n:05}.png")
#    n += 1

# STEP 6: output frames -> video
if skip_to <= 6:
    print("Running ffmpeg")
    ffmpeg_wrapper(f"{pdir}/output", audio_name, f"{name}")