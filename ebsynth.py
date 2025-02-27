import os
import subprocess
from util import sorted_alphanumeric


def ebsynth_wrapper(style_dir, guide_src_dir, guide_tgt_dir, output_dir):
    for f in zip(sorted_alphanumeric(os.listdir(style_dir)), sorted_alphanumeric(os.listdir(guide_src_dir)), sorted_alphanumeric(os.listdir(guide_tgt_dir))):
        args = ['./ebsynth/bin/ebsynth.exe', '-backend', 'cuda',
                '-style', f'{style_dir}/{f[0]}',
                '-guide', f'{guide_src_dir}/{f[1]}', f'{guide_tgt_dir}/{f[2]}',
                '-output', f'{output_dir}/{f[1]}'
                ]
        subprocess.run(args)

#ebsynth_wrapper("finished_frameseqs/scream/0", "vid_pipe/style_masks", "vid_pipe/masks", "vid_pipe/output")