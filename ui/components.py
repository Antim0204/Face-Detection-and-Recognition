
import streamlit as st
from PIL import Image, ImageDraw
import cv2
import numpy as np

def upload_input():
    uploaded_file = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Image", use_container_width=True)
        return uploaded_file
    return None

def camera_input():
    picture = st.camera_input("Capture a face photo")
    if picture:
        img = Image.open(picture).convert("RGB")
        st.image(img, caption="Captured Image", use_container_width=True)
        return picture
    return None

def show_result(result: dict, threshold: float):
    st.markdown("### 🧾 Match Results")
    def draw_bbox(img, bbox):
        if bbox:
            draw = ImageDraw.Draw(img)
            x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
            draw.rectangle([x, y, x + w, y + h], outline="red", width=4)
        return img
    # Handle case: No face detected or matching failed
    if result["score"] == -1 or result["best_match_img"] is None:
        st.error("❌ No human face detected in the input image or no match found in reference images.")
        st.image(result["input_img"], caption="Input Image", use_container_width=True)
        return
    # Draw bounding boxes if available
    input_img = result["input_img"].copy() if hasattr(result["input_img"], 'copy') else result["input_img"]
    best_match_img = result["best_match_img"].copy() if result["best_match_img"] is not None and hasattr(result["best_match_img"], 'copy') else result["best_match_img"]
    if "facial_areas" in result and result["facial_areas"] is not None:
        if "img1" in result["facial_areas"]:
            input_img = draw_bbox(input_img, result["facial_areas"]["img1"])
        if best_match_img is not None and "img2" in result["facial_areas"]:
            best_match_img = draw_bbox(best_match_img, result["facial_areas"]["img2"])
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(input_img, caption="Input Image", use_container_width=True)
        st.metric(label="🔁 Similarity Score", value=f"{result['score']:.2f}%")
        if result["score"] >= threshold:
            st.success(f"✅ Faces match (above {threshold}%)")
        else:
            st.error(f"❌ Faces do not match (below {threshold}%)")
    with col2:
        if best_match_img is not None:
            st.image(best_match_img, caption="Reference Image", use_container_width=True)
        else:
            st.warning("⚠️ No match found or face detection failed in reference images.")
    st.markdown("""
        <style>
        .stImage > img {
            border-radius: 15px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        </style>
    """, unsafe_allow_html=True)