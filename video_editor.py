from moviepy import *
from moviepy.video.fx.crop import crop
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip

def crop_framesplit(source_file, target_dir, size):
    v = VideoFileClip(source_file)
    v = v.subclip(1.25,)
    (w,h) = v.size
    vc = crop(v, width=h, height=h, x_center=w/2, y_center=h/2)
    vf = vc.resize(width=size)



    # For alignment
    #m = AudioFileClip("audio/scream/scream_0s.wav")
    #a = CompositeAudioClip([m])
    #vf.audio = a

    vf.write_images_sequence(f'{target_dir}/%05d.png')