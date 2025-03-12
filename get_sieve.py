import json
import requests
import os
import shutil
import zipfile
from os import makedirs
import sieve_to_mask
# Hard-coded directory to save files
OUTPUT_DIR = "vid_pipe/scream1c/sieve"  # Change this to your desired path


def download_and_extract(url, output_dir, name):
    """Download a zip file from URL and extract it to output_dir"""
    # Get filename from URL (removing query parameters)
    filename = url.split('/')[-1].split('?')[0]
    filepath = os.path.join(output_dir, filename)

    # Download the file
    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)


    makedirs(f"{output_dir}/{name}", exist_ok=True)
    # Extract the zip
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(f"{output_dir}/{name}")

    # Clean up the zip file
    os.remove(filepath)


def process_json(json_input):
    """Process the JSON and handle the downloads"""
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Parse JSON
    data = json.loads(json_input)

    # Download and extract masks
    masks_url = data["masks"]["url"]
    print(f"Processing masks from {masks_url}")
    download_and_extract(masks_url, OUTPUT_DIR, "masks")

    # Download and extract confidences
    confidences_url = data["confidences"]["url"]
    print(f"Processing confidences from {confidences_url}")
    download_and_extract(confidences_url, OUTPUT_DIR, "confidences")

    print(f"Files extracted to {OUTPUT_DIR}")


def main():
    print("Please paste your JSON input below (press Enter twice when done):")

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


if __name__ == "__main__":
    main()