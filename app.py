
import streamlit as st
from config import TEMP_IMAGE_PATH, MATCH_THRESHOLD,REFERENCE_IMAGE_DIR
from ui.components import upload_input, camera_input, show_result
from src.storage import load_reference_image_paths as load_reference_images
from src.face_recognizer import match_face_to_references,check_for_face
import os
from PIL import Image
import logging

# Ensure the reference image directory exists
os.makedirs(REFERENCE_IMAGE_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Face Verification App", layout="centered")
st.markdown("<h1 style='text-align: center;'>Facial Recognition App</h1>", unsafe_allow_html=True)
st.markdown("---")


st.markdown("###  Add a New Reference Face ")
new_reference_file = st.file_uploader(
    "Upload a photo to add it to the reference database.",
    type=['jpg', 'jpeg', 'png'],
    key="ref_uploader"
)

if new_reference_file is not None:
    try:
        # Check if the uploaded image contains a face
        temp_image = Image.open(new_reference_file)
        temp_image_path = os.path.join("outputs", "temp_reference_check.jpg")
        if temp_image.mode != 'RGB':
            temp_image = temp_image.convert('RGB')
        temp_image.save(temp_image_path, "jpeg")

        if not check_for_face(temp_image_path):
            st.error("❌ Reference image not accepted: No human face detected. Please upload an image with a clear human face.")
        else:
            # Create a valid filename and save path
            base_name, _ = os.path.splitext(new_reference_file.name)
            new_filename = f"{base_name}.jpg"
            save_path = os.path.join(REFERENCE_IMAGE_DIR, new_filename)

            # Convert image to RGB (important for saving as JPG)
            if temp_image.mode != 'RGB':
                temp_image = temp_image.convert('RGB')

            # Save the image in the reference directory
            temp_image.save(save_path, 'jpeg')

            logging.info(f"New reference image '{new_filename}' added to the database.")
            st.success(f"✅ Reference image '{new_filename}' added successfully!")
            st.image(temp_image, caption="This image was added as a reference.", width=200)

    except Exception as e:
        logging.error(f"Failed to add reference image: {e}")
        st.error(f"❌ Error adding reference image: {e}")
st.markdown("---")

# ==============================================================================
# EXISTING SECTION: To verify an image
# ==============================================================================
st.markdown("### Step 2: Verify a Face")
# Select input method with big side-by-side buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("📤 Upload Image", use_container_width=True, key="upload_btn"):
        logging.info("Upload Image button clicked.")
        st.session_state["input_method"] = "upload"
with col2:
    if st.button("📷 Use Camera", use_container_width=True, key="camera_btn"):
        logging.info("Use Camera button clicked.")
        st.session_state["input_method"] = "camera"

img = None
if st.session_state.get("input_method") == "upload":
    logging.info("Image input method: Upload")
    img = upload_input()
elif st.session_state.get("input_method") == "camera":
    logging.info("Image input method: Camera")
    img = camera_input()

# If image is successfully uploaded or captured
if img is not None:
    logging.info("Image received. Saving to temp path.")
    # Save the uploaded/captured image
    with open(TEMP_IMAGE_PATH, "wb") as f:
        f.write(img.getbuffer())
    logging.info(f"Image saved at: {TEMP_IMAGE_PATH}")

    # Load reference faces
    references = load_reference_images(REFERENCE_IMAGE_DIR)
    logging.info(f"Loaded {len(references)} reference images.")

    if not references:
        logging.warning("No reference images found in the database.")
        st.warning("No reference images found in the database. Please add one using the uploader above.")
    else:
        logging.info("Starting face matching...")
        # Compare against reference images
        result = match_face_to_references(TEMP_IMAGE_PATH, references)
        logging.info(f"Face matching result: {result}")

        # Show results
        show_result(result, MATCH_THRESHOLD)

st.markdown("""
    <style>
    .stButton > button {
        font-size: 1.5rem;
        height: 4rem;
        width: 100%;
        margin-bottom: 1rem;
        border-radius: 12px;
        background-color: #f0f2f6;
        color: #333;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)