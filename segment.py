import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
from util import sorted_alphanumeric
import warnings

warnings.filterwarnings('ignore')

def segment(source_dir, target_dir, size):
    model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
    torch.set_float32_matmul_precision(['high', 'highest'][0])
    model.to('cuda')
    model.eval()

    # Data settings
    image_size = (size, size)
    transform_image = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    n = 0
    for f in sorted_alphanumeric(os.listdir(source_dir)):
        image = Image.open(f"{source_dir}/{f}")
        input_images = transform_image(image).unsqueeze(0).to('cuda')

        # Prediction
        with torch.no_grad():
            preds = model(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)

        mask.save(f"{target_dir}/{f}")
        n += 1
        if n % 100 == 0 and n > 0:
            print(f" - segmented {n} source images")