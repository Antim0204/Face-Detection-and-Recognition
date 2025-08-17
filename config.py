


REFERENCE_IMAGE_DIR = "data/reference_faces"
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCE_IMAGE_DIR_UI_UPLOAD = os.path.join(BASE_DIR, "data", "reference_faces")
TEMP_IMAGE_PATH = "outputs/temp_uploaded.jpg"

MODEL_NAME =  "Facenet512"  
MATCH_THRESHOLD = 55.0
ENFORCE_DETECTION = True
DETECTOR_BACKEND = "retinaface"  