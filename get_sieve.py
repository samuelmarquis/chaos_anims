import json
import requests
import os
import shutil
import zipfile
from os import makedirs
import sieve_to_mask

OUTPUT_DIR = "vid_pipe/wayelmpromo21/sieve"

def download_and_extract(url, output_dir, name):
    filename = url.split('/')[-1].split('?')[0]
    filepath = os.path.join(output_dir, filename)

    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)


    makedirs(f"{output_dir}/{name}", exist_ok=True)
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(f"{output_dir}/{name}")

    os.remove(filepath)


def process_json(json_input):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = json.loads(json_input)

    masks_url = data["masks"]["url"]
    print(f"Downloading & extracting masks")
    download_and_extract(masks_url, OUTPUT_DIR, "masks")


    confidences_url = data["confidences"]["url"]
    print(f"Downloading & extracting confidences")
    download_and_extract(confidences_url, OUTPUT_DIR, "confidences")

    print(f"Files extracted to {OUTPUT_DIR}")

if __name__ == "__main__":
    print("Paste JSON, double tap enter")

    # Collect multi-line input
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break

    json_input = '\n'.join(lines)

    try:
        process_json(json_input)
    except Exception as e:
        print(f"An error occurred: {str(e)}")