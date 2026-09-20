import streamlit as st
from PIL import Image
import numpy as np
import cv2
from datetime import datetime
import io
from detect import load_model

MAX_MB = 10


def run_detection_inline(pil_image, model, threshold, show_labels):
    MAX_SIZE = 960
    w, h = pil_image.size
    if max(w, h) > MAX_SIZE:
        scale     = MAX_SIZE / max(w, h)
        pil_image = pil_image.resize(
            (int(w * scale), int(h * scale)), Image.LANCZOS)

    img_array = np.ascontiguousarray(
        np.array(pil_image), dtype=np.uint8)
    results   = model(img_array, conf=threshold,
                      device="cpu", verbose=False)
    boxes     = results[0].boxes

    detections = []
    for box in boxes:
        cls = int(box.cls[0])
        if cls != 0:
            continue
        x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
        detections.append({
            "id":         len(detections) + 1,
            "label":      "drone",
            "confidence": round(float(box.conf[0]), 4),
            "bbox":       (x1, y1, x2, y2)
        })

    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
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

    img_rgb       = np.ascontiguousarray(
                        cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB),
                        dtype=np.uint8)
    img_annotated = Image.fromarray(img_rgb)

    avg_conf = 0.0
    if detections:
        avg_conf = (sum(d["confidence"] for d in detections)
                    / len(detections))

    return {
        "filename":        "uploaded_image",
        "image_original":  pil_image,
        "image_annotated": img_annotated,
        "drone_count":     len(detections),
        "avg_confidence":  round(avg_conf, 4),
        "detections":      detections,
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def show_results(result):
    st.markdown("<hr style='margin:20px 0'>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color:#111;margin-bottom:16px'>Detection Results</h3>",
        unsafe_allow_html=True)

    drone_count = result["drone_count"]
    avg_conf    = (f"{result['avg_confidence']*100:.1f}%"
                   if drone_count > 0 else "—")

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    for col, label, value, color in [
        (c1, "Drones Detected", str(drone_count), "#DC2626"),
        (c2, "Avg Confidence",  avg_conf,          "#ea580c"),
        (c3, "Image Size",
         f"{result['image_original'].width}"
         f"×{result['image_original'].height}", "#2563eb"),
        (c4, "Status", "Complete ✓", "#16a34a"),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:#1e1e30;border:1px solid #2d2d45;
                        border-radius:10px;padding:16px 20px;
                        margin-bottom:16px'>
                <div style='font-size:12px;color:#9ca3af;
                            margin-bottom:6px'>{label}</div>
                <div style='font-size:24px;font-weight:700;
                            color:{color}'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

    i1, i2 = st.columns(2, gap="medium")
    with i1:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:14px'>
            <div style='display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:8px'>
                <span style='font-weight:700;color:white;
                             font-size:14px'>Original Image</span>
                <span style='background:#374151;color:#d1d5db;
                             font-size:10px;padding:2px 8px;
                             border-radius:10px'>ORIGINAL</span>
            </div>
        """, unsafe_allow_html=True)
        st.image(result["image_original"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with i2:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:14px'>
            <div style='display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:8px'>
                <span style='font-weight:700;color:white;
                             font-size:14px'>Detection Output</span>
                <span style='background:#DC2626;color:white;
                             font-size:10px;padding:2px 8px;
                             border-radius:10px'>ANNOTATED</span>
            </div>
        """, unsafe_allow_html=True)
        st.image(result["image_annotated"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    d1, d2 = st.columns(2, gap="medium")
    with d1:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:16px'>
            <div style='font-weight:700;color:white;
                        font-size:14px;margin-bottom:12px'>
                Detections</div>
        """, unsafe_allow_html=True)
        if result["drone_count"] > 0:
            st.markdown("""
            <div style='display:flex;font-size:11px;font-weight:700;
                        color:#6b7280;border-bottom:1px solid #2d2d45;
                        padding-bottom:6px;margin-bottom:8px'>
                <span style='width:36px'>#</span>
                <span style='flex:1'>Label</span>
                <span style='width:60px'>Conf.</span>
            </div>
            """, unsafe_allow_html=True)
            for det in result["detections"]:
                st.markdown(f"""
                <div style='display:flex;font-size:13px;padding:6px 0;
                            color:white;border-bottom:1px solid #1a1a2e'>
                    <span style='width:36px;color:#6b7280'>
                        #{det['id']}</span>
                    <span style='flex:1'>drone</span>
                    <span style='width:60px;color:#DC2626;font-weight:700'>
                        {det['confidence']*100:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='color:#6b7280;font-size:13px'>"
                "No drones detected in this image.</div>",
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:16px'>
            <div style='font-weight:700;color:white;
                        font-size:14px;margin-bottom:12px'>
                Confidence Breakdown</div>
        """, unsafe_allow_html=True)
        if result["drone_count"] > 0:
            for det in result["detections"]:
                pct = int(det["confidence"] * 100)
                st.markdown(f"""
                <div style='margin-bottom:12px'>
                    <div style='font-size:13px;color:#9ca3af;
                                margin-bottom:5px'>
                        Drone #{det['id']}</div>
                    <div style='background:#2d2d45;border-radius:6px;
                                height:24px;overflow:hidden'>
                        <div style='background:#DC2626;height:100%;
                                    width:{pct}%;border-radius:6px;
                                    display:flex;align-items:center;
                                    justify-content:flex-end;
                                    padding-right:8px'>
                            <span style='font-size:12px;font-weight:700;
                                         color:white'>{pct}%</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='color:#6b7280;font-size:13px'>"
                "No drones to display.</div>",
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    img_bytes = io.BytesIO()
    result["image_annotated"].save(img_bytes, format="JPEG", quality=95)
    img_bytes.seek(0)
    st.download_button(
        label     = "⬇  Download Annotated Result",
        data      = img_bytes,
        file_name = f"annotated_{result['filename']}",
        mime      = "image/jpeg",
        use_container_width=True
    )


def render(model):
    ct, cs = st.columns([4, 1])
    with ct:
        st.markdown(
            "<h2 style='margin:0;color:#111'>Upload &amp; Detect</h2>",
            unsafe_allow_html=True)
        st.caption("Upload an image to run drone detection")
    with cs:
        st.markdown("""
        <div style='display:flex;justify-content:flex-end;
                    align-items:center;gap:6px;padding-top:6px'>
            <div style='width:10px;height:10px;border-radius:50%;
                        background:#16a34a'></div>
            <span style='font-size:12px;color:#6b7280'>Model Ready</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:6px 0 20px 0'>", unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:24px'>
            <div style='font-weight:700;font-size:16px;color:white;
                        margin-bottom:4px'>Upload Image</div>
            <div style='font-size:12px;color:#6b7280;margin-bottom:16px'>
                Supported: JPG, JPEG, PNG &nbsp;•&nbsp; Max: 10 MB
            </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose image file",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

        file_valid = False
        pil_image  = None

        if uploaded is not None:
            size_mb = uploaded.size / (1024 * 1024)
            if size_mb > MAX_MB:
                st.error(
                    f"❌ File too large ({size_mb:.1f} MB). Max 10 MB.")
            else:
                try:
                    pil_image  = Image.open(uploaded).convert("RGB")
                    file_valid = True
                    st.markdown(f"""
                    <div style='background:#052e16;
                                border:1px solid #166534;
                                border-radius:8px;padding:10px 14px;
                                margin-top:8px;font-size:13px'>
                        📄 &nbsp;
                        <b style='color:white'>{uploaded.name}</b><br>
                        <span style='color:#4ade80'>
                            {size_mb:.1f} MB &nbsp;|&nbsp; ✓ Valid
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Cannot read file: {e}")

        st.markdown("""
        <div style='font-weight:700;font-size:15px;color:white;
                    margin:18px 0 8px 0'>Detection Settings</div>
        """, unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:13px;color:#9ca3af;margin-bottom:4px'>"
            "Confidence Threshold</div>",
            unsafe_allow_html=True)

        threshold = st.slider(
            "Confidence Threshold",
            min_value=0.10, max_value=1.00,
            value=float(st.session_state["threshold"]),
            step=0.05,
            label_visibility="collapsed"
        )
        st.session_state["threshold"] = threshold

        sc, tc = st.columns([3, 1])
        with sc:
            st.markdown(
                "<div style='font-size:13px;color:#9ca3af;"
                "padding-top:10px'>"
                "Show Confidence Labels</div>",
                unsafe_allow_html=True)
        with tc:
            show_labels = st.toggle(
                "Show Labels",
                value=bool(st.session_state["show_labels"]),
                label_visibility="collapsed"
            )
        st.session_state["show_labels"] = show_labels

        st.markdown(
            "<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        run_btn = st.button(
            "🔍  Run Detection",
            type="primary",
            disabled=not file_valid,
            use_container_width=True
        )
        st.caption("⚡ Estimated processing time: ~2-5 seconds")

    with right:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:24px'>
            <div style='font-weight:700;font-size:16px;color:white;
                        margin-bottom:14px'>Image Preview</div>
        """, unsafe_allow_html=True)

        if pil_image is not None:
            st.image(pil_image, use_container_width=True)
            st.markdown(
                f"<div style='font-size:12px;color:#4ade80;"
                f"margin-top:8px'>✓ Image loaded and ready</div>"
                f"<div style='font-size:12px;color:#6b7280'>"
                f"Resolution: {pil_image.width}×{pil_image.height}"
                f"</div>",
                unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='height:280px;background:#111827;
                        border:2px dashed #374151;border-radius:10px;
                        display:flex;align-items:center;
                        justify-content:center;
                        color:#4b5563;font-size:14px'>
                Upload an image to preview it here
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Detection — outside columns
    if run_btn and file_valid and pil_image is not None:
        try:
            result = run_detection_inline(
                pil_image, model, threshold, show_labels)
            result["filename"] = uploaded.name
            st.session_state["last_result"] = result
            st.session_state["history"].append(result)
            show_results(result)
        except Exception as e:
            st.error(f"❌ Detection failed: {e}")
            st.exception(e)

st.session_state.setdefault("threshold", 0.5)
st.session_state.setdefault("show_labels", True)
st.session_state.setdefault("history", [])
st.session_state.setdefault("last_result", None)

model = load_model()
render(model)