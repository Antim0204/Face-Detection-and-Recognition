import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import logging
import os

LOG_FILE = "outputs/logs.txt"

def compute_cosine_similarity(embedding1, embedding2):
    """Returns cosine similarity percentage."""
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    return round(similarity * 100, 2)

def setup_logging():
    """Configure logging to file."""
    os.makedirs("outputs", exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

def log_match(reference_name, score, result):
    """Write match result to log file."""
    logging.info(f"Compared with: {reference_name} | Score: {score:.2f}% | Match: {result}")
