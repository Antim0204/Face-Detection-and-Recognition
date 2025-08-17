# Face Verification App

A modern, interactive web application for face verification using DeepFace and Streamlit. Users can upload or capture a face image, which is then compared against a database of reference faces to verify identity.

---

## Table of Contents
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [System Design](#system-design)
- [Flow Chart](#flow-chart)
- [Folder Structure](#folder-structure)
- [Code Explanation](#code-explanation)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Customization](#customization)

---

## Features
- Upload or capture face images via webcam.
- Compare input image against reference images using DeepFace.
- Display similarity score and match result.
- Visualize detected face regions with bounding boxes.
- Modern, responsive UI with Streamlit.

---

## Architecture Overview
- **Frontend/UI:** Streamlit web interface for user interaction.
- **Backend/Recognition:** DeepFace for face detection and verification.
- **Storage:** Reference images and logs managed in dedicated folders.
- **Utilities:** Helper functions for logging, similarity computation, and image management.

---

## System Design
1. **User Input:**
   - Users choose between uploading an image or capturing one via webcam.
   - The selected image is displayed for confirmation.
2. **Face Matching:**
   - The input image is saved temporarily.
   - All reference images are loaded from the `data/reference_faces/` directory.
   - Each reference image is compared to the input using DeepFace's `verify` function.
   - The best match is selected based on a normalized similarity score.
3. **Result Display:**
   - The UI shows the input and best match images side-by-side.
   - Bounding boxes highlight detected face regions.
   - Similarity score and match status are displayed.
   - Optionally, logs are written for each comparison.

---

## Flow Chart

```
User
  |
  v
Streamlit UI
  |
  v
Temporary Storage
  |
  v
Reference Images
  |
  v
Storage Loader
  |
  v
Face Recognizer (DeepFace)
  |
  v
Results: Images, Score, Bounding Box
  |
  v
User
```

---

## Folder Structure
```
Version3 Working/
│
├── app.py                  # Main Streamlit app
├── config.py               # Configuration variables
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── data/
│   └── reference_faces/    # Reference images for matching
│
├── outputs/
│   ├── logs.txt            # Log file for matches
│   └── temp_uploaded.jpg   # Temporary image storage
│
├── src/
│   ├── face_recognizer.py  # Face matching logic
│   ├── storage.py          # Reference image loading
│   ├── utils.py            # Utility functions
│   └── __init__.py
│
└── ui/
    ├── components.py       # Streamlit UI components
    └── __init__.py
```

---

## Code Explanation
### `app.py`
- Entry point for the Streamlit app.
- Sets up the UI, handles user input, and coordinates the matching workflow.
- Uses session state to manage button clicks and input method.
- Displays results with custom styling.

### `config.py`
- Centralizes configuration for paths, model selection, thresholds, and detection settings.

### `src/face_recognizer.py`
- Contains `match_face_to_references`, which:
  - Iterates over reference images.
  - Uses DeepFace to verify each image pair.
  - Tracks the best match and its facial area for bounding box display.
  - Returns all relevant data for UI display.

### `src/storage.py`
- Loads all valid image paths from the reference directory.

### `src/utils.py`
- Provides utility functions for cosine similarity, logging, and log setup.

### `ui/components.py`
- Defines UI components for image upload, camera input, and result display.
- Draws bounding boxes on images using PIL.
- Uses Streamlit columns for a modern, side-by-side layout.

---

## Setup & Installation
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd Version3\ Working
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **(macOS only) Install Watchdog for better file watching:**
   ```sh
   xcode-select --install
   pip install watchdog
   ```
4. **Run the app:**
   ```sh
   streamlit run app.py
   ```

---

## Usage
- Choose "Upload Image" or "Use Camera" via the large buttons.
- Upload or capture a face image.
- The app will compare the input against all reference faces and display the best match, similarity score, and bounding boxes.

---

## Dependencies
- `deepface` - Face recognition and verification.
- `streamlit` - Web UI framework.
- `opencv-python-headless` - Image processing.
- `scikit-learn` - Similarity computation.
- `matplotlib` - (optional, for visualization).
- `tf-keras` - Deep learning backend.

---

## Customization
- **Add reference images:** Place `.jpg`, `.jpeg`, or `.png` files in `data/reference_faces/`.
- **Change model/backend:** Edit `MODEL_NAME` and `DETECTOR_BACKEND` in `config.py`.
- **Adjust threshold:** Modify `MATCH_THRESHOLD` in `config.py` for stricter or looser matching.

---

## License
MIT License (or specify your own)

---

## Author
Your Name (replace with your details)

---

## Notes
- The flow chart above uses Mermaid syntax. You can visualize it in Markdown viewers that support Mermaid, or use [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor/) for a graphical view.
