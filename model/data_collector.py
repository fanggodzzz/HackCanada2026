import os
import json
import time
import random
import requests
import numpy as np
from ddgs import DDGS
from PIL import Image
from io import BytesIO

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def is_valid_image(img):
    # remove tiny images
    if img.width < 200 or img.height < 200:
        return False

    # remove single-color / blank images
    arr = np.array(img)
    if arr.std() < 10:
        return False

    return True


def download_image(url, save_path):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))

        if img.mode != "RGB":
            img = img.convert("RGB")

        if not is_valid_image(img):
            return False

        img.save(save_path, "JPEG", quality=90)

        return True

    except:
        return False


def collect_data(num_images=200):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    info_path = os.path.join(base_dir, "disease_info.json")
    dataset_dir = os.path.join(base_dir, "dataset")

    with open(info_path, "r") as f:
        diseases_info = json.load(f)

    os.makedirs(dataset_dir, exist_ok=True)

    for info in diseases_info:

        disease = info["disease"]
        disease_dir = os.path.join(dataset_dir, disease.replace(" ", "_"))

        os.makedirs(disease_dir, exist_ok=True)

        print(f"\nCollecting images for: {disease}")

        # better query for real dermatology photos
        query = f"{disease} dermatology clinical photo skin lesion close-up"

        download_count = 0

        try:
            with DDGS() as ddgs:

                results = ddgs.images(
                    query,
                    max_results=num_images * 5,
                    safesearch="off"
                )

                for r in results:

                    if download_count >= num_images:
                        break

                    url = r.get("image")
                    if not url:
                        continue

                    save_path = os.path.join(
                        disease_dir,
                        f"{download_count:03d}.jpg"
                    )

                    if download_image(url, save_path):

                        download_count += 1

                        if download_count % 10 == 0:
                            print(
                                f"Downloaded {download_count}/{num_images}"
                            )

                    # random delay to avoid rate limit
                    time.sleep(random.uniform(0.2, 0.6))

        except Exception as e:
            print(f"Search error for {disease}: {e}")

        print(
            f"Completed {disease}: {download_count} images downloaded."
        )


if __name__ == "__main__":

    print("Starting Data Collection...")
    collect_data(20)