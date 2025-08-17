import os
from config import REFERENCE_IMAGE_DIR

def load_reference_image_paths(reference_dir=REFERENCE_IMAGE_DIR):
    reference_paths = []

    if not os.path.exists(reference_dir):
        return reference_paths

    for filename in os.listdir(reference_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            full_path = os.path.join(reference_dir, filename)
            reference_paths.append(full_path)

    return reference_paths
