import os
from PIL import Image
from util import sorted_alphanumeric
from video_editor import crop_framesplit
from segment import segment
from fractal_mask import mask
from ebsynth import ebsynth_wrapper
from ffmpeg_wrapper import ffmpeg_wrapper
from os import makedirs

skip_to = 6

input_vid = "source_video/scream11.mov"
style_dir = "finished_frameseqs/scream/11"

base = "vid_pipe"
name = "scream11"
pdir = f"{base}/{name}"
audio_name = "audio/scream/scream_11s.wav"
res = 512

makedirs(f"{pdir}/src_frames", exist_ok=True)
makedirs(f"{pdir}/masks", exist_ok=True)
makedirs(f"{pdir}/style", exist_ok=True)
makedirs(f"{pdir}/style_masks", exist_ok=True)
makedirs(f"{pdir}/output", exist_ok=True)

# STEP 1: src video -> square-cropped frame sequences
if skip_to <= 1:
    print("Splitting frames")
    crop_framesplit(f"{input_vid}", f"{pdir}/src_frames", 512)


# STEP 2: source frames -> source mask
if skip_to <= 2:
    print("Segmenting source")
    segment(f"{pdir}/src_frames", f"{pdir}/masks", 512)

# STEP 3: resize style
if skip_to <= 3:
    print("Resizing style")
    for f in sorted_alphanumeric(os.listdir("finished_frameseqs/scream/11")):
        image = Image.open(f"finished_frameseqs/scream/11/{f}").resize((512,512)).save(f"{pdir}/style/{f}")

# STEP 4: style frames -> style mask
if skip_to <= 4:
    print("Masking style")
    mask(f"{pdir}/style", f"{pdir}/style_masks", 512)

# STEP 5: ebsynth :: style frames -> style masks -> source masks -> output frames
if skip_to <= 5:
    print("Running ebsynth")
    ebsynth_wrapper(f"{pdir}/style",
                    f"{pdir}/style_masktest",
                    f"{pdir}/masks",
                    f"{pdir}/bad_out")

#n = 0
#for f in sorted_alphanumeric(os.listdir(f"{pdir}/bad_out")):
#    image = Image.open(f"{pdir}/bad_out/{f}").save(f"{pdir}/output/{n:05}.png")
#    n += 1

# STEP 6: output frames -> video
if skip_to <= 6:
    print("Running ffmpeg")
    ffmpeg_wrapper(f"{pdir}/bad_out", audio_name, "scream11")