from deepface import DeepFace
from PIL import Image
from config import MODEL_NAME, DETECTOR_BACKEND,ENFORCE_DETECTION



def check_for_face(image_file, detector_backend="retinaface"):
    """
    Checks if the given image contains at least one human face.
    Returns True if a face is detected, False otherwise.
    """
    try:
        faces = DeepFace.extract_faces(img_path=image_file, detector_backend=detector_backend, enforce_detection=True)
        return len(faces) > 0
    except Exception as e:
        return False
    
def normalize_score(distance: float, model: str = "ArcFace") -> float:
    max_dist_map = {
        "ArcFace": 1.2,
        "Facenet512": 1.4,
        "VGG-Face": 1.5,
        "SFace": 1.1,
        "OpenFace": 1.0
    }
    max_dist = max_dist_map.get(model, 1.4)
    return max(0, 100 * (1 - distance / max_dist))
    


def match_face_to_references(input_img_path: str, reference_img_paths: list) -> dict:
    best_score = -1
    best_match_img = None
    best_match_path = None
    best_facial_areas = None

    for ref_img_path in reference_img_paths:
        try:
            result = DeepFace.verify(
                img1_path=input_img_path,
                img2_path=ref_img_path,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=ENFORCE_DETECTION,
                normalization="Facenet"
            )
            threshold = result["threshold"]
            distance = result["distance"]
            print(f"Model Distance: {distance}, Model Threshold: {threshold}")

            score = normalize_score(distance, MODEL_NAME)
            print(f"Matching {input_img_path} with {ref_img_path}: score={score}")
            if score > best_score:
                best_score = score
                best_match_path = ref_img_path
                best_facial_areas = result.get("facial_areas", None)
        except Exception as e:
            print(f"[Warning] Matching failed with {ref_img_path}: {str(e)}")

    input_img = Image.open(input_img_path)
    if best_match_path:
        best_match_img = Image.open(best_match_path)

    return {
        "score": best_score,
        "best_match_img": best_match_img,
        "best_match_path": best_match_path,
        "input_img": input_img,
        "facial_areas": best_facial_areas
    }
