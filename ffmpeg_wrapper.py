import subprocess
def ffmpeg_wrapper(frameseq_dir, audio_name,output_name):
    args = ['C:\Windows\System32\wsl.exe',
            'ffmpeg', '-y',
            '-framerate', '30',
            '-i', f'{frameseq_dir}/%05d.png',
            '-i', f'audio/{audio_name}.wav',
            '-map', '0:v', '-map', '1:a',
            '-b:a', '320k', '-c:v', 'libx264',
            '-strict', '2', '-preset', 'slow', '-pix_fmt', 'yuv420p',
            '-shortest',
            '-f', 'mp4',
            f'media/{output_name}.mp4']
    #yes = subprocess.Popen(['C:\Windows\System32\wsl.exe', 'yes'], stdout=subprocess.PIPE)
    subprocess.run(args, shell=True)

#ffmpeg_wrapper('finished_frameseqs/setmefree_2c', 'setmefree/setmefree_2s', 'setmefree_2c')