import subprocess
import warnings

from diffusers.utils import load_image
import torch, os
from shutil import copyfile
import re

from ffmpeg_wrapper import ffmpeg_wrapper


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def calculate_overlap(overlap_len, tran_point, interp_len, path_s, path_e): #interp len must be one less than the number of new frames
    tran_start = (tran_point - overlap_len) - interp_len
    last = os.path.join(path_s, sorted_alphanumeric(os.listdir(path_s))[tran_start]) #put plus one here and set interp len back to what its supposed to be.. later

    print(path_s + last)
    first = os.path.join(path_e, sorted_alphanumeric(os.listdir(path_e))[tran_point])
    print(path_e + first)
    return last, first
def copyrename(number, project, makevid = False):
    #input("WARNING: ARE YOU SURE? DO YOU REALLY WANT TO COPY OVER DIFFUSION WITH CHAOTICA IMAGES?")
    ipath = f"../../Projects/Visual/Chaotica/anims/{project}/{number}/"
    opath = f"finished_frameseqs/{project}/{number}/"
    counter = 0
    n = len([x for x in os.listdir(ipath) if 'mp4' not in x])
    try:
        os.mkdir(opath)
    except:
        print(f"{opath} already exists")
    for fn in os.listdir(ipath):
        if "mp4" in fn:
            continue
        if counter % 100 == 99: print(f"copying {counter+1}/{n}...")
        init_image = load_image(ipath + fn)
        #switch these lines for disjoint partial sequences
        #init_image.save(f"{opath}{fn[6:]}")
        init_image.save(f"{opath}{str(counter).zfill(5)}.png")
        counter += 1
    print(f"copied {n}/{n}")
    if len(os.listdir(opath)) % 30 != 0:
        print("WARNING: clip length is not a multiple of 30. Double check frame count.")
        input("Press enter to continue")
    if makevid: ffmpeg_wrapper(opath, f"{project}/{project}_{number}s", f"{project}_{number}")



path = "finished_frameseqs/"
ipath = "finished_frameseqs/INTERP"
to_merge = ["goodbyeporkpie/",       "phylogen_intro/",  "phylogen_drop1/",      "phylogen_breakdown1/",
            "phylogen_transition1/", "phylogen_verse1/", "phylogen_chorus1/",    "phylogen_transition2/",
            "phylogen_verse2/",      "phylogen_drop2/",  "phylogen_breakdown2/", "phylogen_transition3/",
            "phylogen_endbw/",       "boardwarp_verse/", "boardwarp_drop/",      "boardwarp_pre/",
            "scream_1/",             "scream_2/",        "scream_3/",            "scream_4/",
            "wayelm_1/",             "wayelm_2/",        "wayelm_3/",            "wayelm_4/",
            "wayelm_5/",             "dancing_1/",       "dancing_2/",           "atomic_1/",
            "atomic_2/",             "atomic_3/",        "atomic_4/"]


interp_list = ["goodbyeporkpie0", "phylogen0", "phylogen1", "phylogen2",
               "phylogen3",       "phylogen4", "phylogen5", "phylogen6",
               "phylogen7",       "phylogen8", "phylogen9", "phylogen10",
               "phylogen11",      "board0",    "board1",    "board2",
               "scream0",         "scream1",   "scream2",   "scream3",
               "wayelm1",         "wayelm2",   "wayelm3",   "wayelm4",
               "wayelm5",         "dancing1",  "dancing2",  "atomic1",
               "atomic2",         "atomic3"] #TODO having this list is fucking insane. remove it

overlap_lengths = [56,30,0, 15,0, 15,30,30,0, 30,30, 30, 19, 15, 30, 0,  30, 30, 30, 30, 30, 0,  0,  0,  30, 30, 30, 0,  30, 30]
tran_points     = [30,12,0, 12,0, 12,12,18,0, 12,20, 15, 18, 13, 14, 0,  2,  15, 10, 10, 14, 0,  0,  0,  18, 23, 21, 0,  12, 5]
                #n 0g 1p 2p 3p 4p 5p 6p 7p 8p 9p 10p 11p 12p 13b 14b 15b 16s 17s 18s 19s 20w 21w 22w 23w 24d 25d 26a 28a 29a 30a
interp_len      = 8 #INTERP FRAMES - 1. DON'T QUESTION IT
out = "../frame-interpolation/photos/interpolated_frames"

copyrename(5, 'scream', makevid=True)

exit(0)
#copyrename(to_merge[-1][:-1], True)
n = []
paths_s = []
paths_e = []
last = "kill me now"
for i in range(len(overlap_lengths)):
    counter = 0
    print(f"pair {i}:")
    paths, pathe = calculateOverlap(overlap_lengths[i],tran_points[i],
                                    interp_len,
                                    path+to_merge[i], path+to_merge[i+1])
    paths_s.append(paths)
    paths_e.append(pathe)
    s = load_image(paths)
    e = load_image(pathe)
    try:
        os.mkdir(os.path.join(path, f"INTERP/{interp_list[i]}")) #control flow hack. this will fail if the directory exists
        s.save("../frame-interpolation/photos/0.png")
        e.save("../frame-interpolation/photos/1.png")
        input("Go run frame-interp... enter to continue AFTER it has finished")
        """
        arg = "C:/Users/Sam/.conda/envs/frame-interpolation/python.exe Y:/Dropbox/Code/frame-interpolation/main.py --pattern \"photos\" --model_path Y:/Dropbox/Code/frame-interpolation/pretrained_models/film_net/Style/saved_model --times_to_interpolate 5"
        import subprocess
        subprocess.call(arg)
        """
        for imga in os.listdir(out):
            img = load_image(os.path.join(out, imga))
            img.save(f"finished_frameseqs/INTERP/{interp_list[i]}/{counter}.png")
            counter += 1
    except:
        print(f"Interp frames already generated. Delete the INTERP/{interp_list[i]} folder to generate iframes")


counter = 0
skipped = 0
start_encountered = True
print(len(to_merge))
for i in range(len(to_merge)):
    skipped = 0
    print(f"Copying {to_merge[i]} to start=out/{str(counter).zfill(5)}.png")
    wdir = os.path.join(path, to_merge[i])
    for f in sorted_alphanumeric(os.listdir(wdir)):
        #print(os.path.join(wdir,f), "\n", paths_s[i])
        if 'mp4' in f:
            continue
        if not start_encountered:
            skipped += 1
            if os.path.join(wdir,f) == paths_e[i-1]: start_encountered = True
            continue
        if to_merge[i] != to_merge[-1] and os.path.join(wdir,f) == paths_s[i]:
            #print(f"encountered {f}, ending WITHOUT copying")
            break
        copyfile(os.path.join(wdir, f), "out/" + str(counter).zfill(5) + ".png")
        #img = load_image(os.path.join(wdir, f))
        #img.save("out/" + str(counter).zfill(5) + ".png")
        counter += 1
    if to_merge[i] != to_merge[-1]:
        #print(f"beginning interpolation, skipped {skipped} frames")
        print(f"Copying {interp_list[i]} to start=out/{str(counter).zfill(5)}.png")
        wdir = os.path.join(ipath, f"{interp_list[i]}")
        for f in sorted_alphanumeric(os.listdir(wdir)):
            copyfile(os.path.join(wdir, f), "out/" + str(counter).zfill(5) + ".png")
            #img = load_image(os.path.join(wdir, f))
            #img.save("out/" + str(counter).zfill(5) + ".png")
            counter += 1
    start_encountered = False

#ffmpeg_wrapper("out/", "fullbodyheadache/thorjnsetstereo","fullbodysprainset")