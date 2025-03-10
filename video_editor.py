from moviepy import *
from moviepy.video.fx.crop import crop
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip

def crop_framesplit(source_file, target_dir, size):
    v = VideoFileClip(source_file)
    v = v.subclip(63,90)
    (w,h) = v.size
    vc = crop(v, width=h*0.75, height=h*0.75, x_center=w/2, y_center=h/2)
    vf = vc.resize(width=size)
    vf.write_images_sequence(f'{target_dir}/%05d.png')

if __name__ == '__main__':
    None