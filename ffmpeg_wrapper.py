import subprocess
from os.path import exists


def ffmpeg_wrapper(frameseq_dir, audio_name, output_name, framerate=0, pattern="%05d", comp_rat=30):
    args = ['C:\Windows\System32\wsl.exe',
            'ffmpeg', '-y',
            '-framerate', f'{framerate}',
            '-thread_queue_size', '1024',
            '-i', f'{frameseq_dir}/{pattern}.png',
            '-thread_queue_size', '1024',
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

    outfile = "scream5_7"
    if exists(f"media/{outfile}.mp4"):
        print(f"WARNING: DO YOU REALLY WANT TO OVERWRITE {outfile}.mp4")
        d = input("ENTER '!x' TO OVERWRITE\n")
        if d != "!x":
            print("ABORTING")
            exit(1)

    ffmpeg_wrapper('vid_pipe/scream5/output4',
                   'audio/scream/5s.wav',
                   outfile,
                   framerate=24,
                   pattern="%05d",
                   comp_rat=20)