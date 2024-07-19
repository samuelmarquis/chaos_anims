import random

from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
import torch, os
from compel import Compel, PromptParser
import wave, ctypes
import numpy as np
import warnings


def itfalse():
    yield False
"""
def img_var():
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-unclip-small", torch_dtype=torch.float16)



    pipe.safety_checker = lambda images, clip_input: (images, itfalse())
    pipe.to("cuda")
    compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)
    while True:
        x = random.Random().randint(0, 100000000)
        with open('prompt.txt','r') as file:
            prompt1 = file.read()
            print(f"Loaded prompt.txt: {prompt1}")
            print(f"Loaded image: in/wisiatsgm/{x%10}.png")
            cond1 = compel.build_conditioning_tensor(prompt1)

            init_image = load_image(f"in/lys1024.png")

            image = pipe(init_image, guidance_scale=16, prompt_embeds=cond1, num_inference_steps=50).images[0]
            image.save(f"singlediffuseout/lys/{x}.png")"""

def diffuse_single():

    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.safety_checker = lambda images, clip_input: (images, itfalse())
    pipe = pipe.to("cuda")
    compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)
    x = 0
    while True:
        x = random.Random().randint(0, 100000000)
        with open('prompt.txt','r') as file:
            prompt1 = file.read()
            print(f"Loaded prompt.txt: {prompt1}")
            print(f"Loaded image: in/lys/{x%2}.png")
            cond1 = compel.build_conditioning_tensor(prompt1)
            init_image = load_image(f"in/lys/{x%2}.png")
            image = pipe(prompt_embeds=cond1,
                         guidance_scale=1,
                         image=init_image,
                         strength=0.6,
                         num_inference_steps=40
                         ).images[0]
            image.save(f"singlediffuseout/lys/{x}.png")
            print(f"Saved image {x}.png")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    diffuse_single()

diffuse_single()
exit(0)

song = wave.open("audio/atomicd_4.wav") #give a mono file to make life easier

loudest = 5000000 #normalized to 0db? try 6000000
sr = song.getframerate()
print(sr)
sd = song.getsampwidth()
print(sd)

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.safety_checker = lambda images, clip_input: (images, itfalse())
pipe = pipe.to("cuda")
compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)
prompt1 = "circuit board technology crystal good cable management "
cond1 = compel.build_conditioning_tensor(prompt1)
#for i in range(8, 11):
if True:
    #if i == 7: continue
    path = f"finished_frameseqs/scream_1/"
    opath = f"finished_frameseqs/scream_1d/"
    print(path)
    counter = 0
    rmslist = []
    for fn in os.listdir(path):
        ab = song.readframes(int(sr/30))
        if counter < -1: # continue from frame:
            counter += 1
            continue
        fv = [x for x in ab]
        nv = []
        assert(len(fv)/3 == int(len(fv)/3)) #sanity check for 24-bit wav
        for i in range(0,int(len(fv)/3)):
            n1 = i*3
            n2 = i*3 + 1
            n3 = i*3 + 2
            unsigned = fv[n3]<<16 | fv[n2]<<8 | fv[n1] #hardcode endianness
            nv.append(unsigned if not (unsigned & 0x800000) else unsigned - 0x1000000) # restore sign

        n2v = [x**2 for x in nv] #rms loudness
        rms = np.sqrt(np.mean(n2v))
        lstren = min(rms/loudest, 0.85) #1.0 completely disregards input image so we cap slightly lower

        print("rendering frame " + str(counter) + " with strength = " + str(lstren))

        init_image = load_image(path + fn)

        if(counter > 93 and counter < 104):
            image = pipe(prompt_embeds=cond1, guidance_scale = 1, image=init_image, strength=0.7, num_inference_steps=50, seed=0).images[0]
            image.save(opath + fn)
        else:
            #rmslist.append(rms) #for finding loudest in combination with if(False) above
            init_image.save(opath + fn)
        counter += 1

print(rmslist)