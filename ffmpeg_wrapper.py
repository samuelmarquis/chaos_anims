import subprocess

def ffmpeg_wrapper(frameseq_dir, audio_name,output_name, framerate=0, pattern="%05d", comp_rat=30):
    args = ['C:\Windows\System32\wsl.exe',
            'ffmpeg', '-y',
            '-framerate', f'{framerate}',
            '-i', f'{frameseq_dir}/{pattern}.png',
            '-i', f'{audio_name}',
            '-map', '0:v', '-map', '1:a',
            '-b:a', '320k', '-c:v', 'libx264', '-crf', f'{comp_rat}',
            '-strict', '2', '-preset', 'slow', '-pix_fmt', 'yuv420p',
            '-shortest',
            '-f', 'mp4',
            f'media/{output_name}.mp4']
    #yes = subprocess.Popen(['C:\Windows\System32\wsl.exe', 'yes'], stdout=subprocess.PIPE)
    subprocess.run(args, shell=True)

if __name__ == '__main__':
    input("ARE YOU SURE YOU INCREMENTED THE OUTPUT NAME?")
    ffmpeg_wrapper('vid_pipe/scream11/output',
                   'audio/scream/11s.wav',
                   'scream11_10',
                   framerate=24,
                   pattern="frame0%05d",
                   comp_rat=20)