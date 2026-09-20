import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import streamlit as st
from ultralytics import YOLO

MODEL_PATH = "model/best.pt"


@st.cache_resource
def load_model(model_path: str = MODEL_PATH) -> YOLO:
    import os
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at '{model_path}'. "
            "Please place best.pt in the model/ folder."
        )
    return YOLO(model_path)


def run_detection(
    image: Image.Image,
    model: YOLO,
    threshold: float = 0.5,
    show_labels: bool = True
) -> dict:

    # Resize large images before inference — prevents timeout
    MAX_SIZE = 1280
    w, h = image.size
    if max(w, h) > MAX_SIZE:
        scale = MAX_SIZE / max(w, h)
        image = image.resize((int(w*scale), int(h*scale)), Image.LANCZOS)

    image_array = np.array(image)
    results     = model(image_array, conf=threshold, verbose=False)
    boxes       = results[0].boxes

    detections = []
    for i, box in enumerate(boxes):
        cls = int(box.cls[0])
        if cls != 0:
            continue
        x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
        confidence = float(box.conf[0])
        detections.append({
            "id":         i + 1,
            "label":      "drone",
            "confidence": round(confidence, 4),
            "bbox":       (x1, y1, x2, y2)
        })

    annotated_array  = draw_boxes(image_array.copy(), detections, show_labels)
    image_annotated  = Image.fromarray(annotated_array)

    avg_conf = 0.0
    if detections:
        avg_conf = sum(d["confidence"] for d in detections) / len(detections)

    return {
        "filename":        "uploaded_image",
        "image_original":  image,
        "image_annotated": image_annotated,
        "drone_count":     len(detections),
        "avg_confidence":  round(avg_conf, 4),
        "detections":      detections,
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def draw_boxes(
    image_array: np.ndarray,
    detections: list,
    show_labels: bool = True
) -> np.ndarray:

    # Force contiguous writable array — fixes OpenCV on Python 3.14
    img_bgr = cv2.cvtColor(
        np.ascontiguousarray(image_array, dtype=np.uint8),
        cv2.COLOR_RGB2BGR
    )

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        conf  = det["confidence"]
        label = f"drone {conf:.2f}"

        cv2.rectangle(img_bgr, (x1,y1), (x2,y2), (0,0,220), 2)

        if show_labels:
            (tw, th), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
            cv2.rectangle(img_bgr,
                          (x1, y1-th-8), (x1+tw+6, y1),
                          (0,0,220), -1)
            cv2.putText(img_bgr, label, (x1+3, y1-4),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55, (255,255,255), 1)

    return np.ascontiguousarray(
        cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB),
        dtype=np.uint8
    )