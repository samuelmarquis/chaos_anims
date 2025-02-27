from video_editor import crop_framesplit
from segment import segment
from fractal_mask import mask
from ebsynth import ebsynth_wrapper
from ffmpeg_wrapper import ffmpeg_wrapper
from os import makedirs

input_vid = ""
style_dir = ""

base = "vid_pipe"
name = "scream0"
pdir = f"{base}/{name}"
audio_name = "audio/scream/scream_0s.wav"

makedirs(f"{pdir}/src_frames", exist_ok=True)
makedirs(f"{pdir}/masks", exist_ok=True)
makedirs(f"{pdir}/style", exist_ok=True)
makedirs(f"{pdir}/style_masks", exist_ok=True)
makedirs(f"{pdir}/output", exist_ok=True)

# src video -> square-cropped frame sequences
crop_framesplit(f"{input_vid}", f"{pdir}/src_frames")

# source frames -> source mask
segment(f"{pdir}/src_frames", f"{pdir}/masks")

# style frames -> style mask
mask(f"{style_dir}", f"{pdir}/style_masks")

# style frames -> style masks -> source masks -> output frames
ebsynth_wrapper(f"{style_dir}",
                f"{pdir}/style_masks",
                f"{pdir}/masks",
                f"{pdir}/output")

# output frames -> video
ffmpeg_wrapper(f"{pdir}/output", audio_name, name)