from moviepy import *
from moviepy.video.fx.crop import crop
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip

def crop_framesplit(source_file, target_dir, size=None):
    v = VideoFileClip(source_file)
    #v = v.subclip(0,5)
    #(w,h) = v.size
    #vc = crop(v, width=h*0.75, height=h*0.75, x_center=w/2, y_center=h/2)
    #vf = vc.resize(width=size)
    v.write_images_sequence(f'{target_dir}/%05d.png')

if __name__ == '__main__':
    name = "scream1c"
    crop_framesplit(f"source_video/{name}.mp4", f"vid_pipe/{name}/src_frames")