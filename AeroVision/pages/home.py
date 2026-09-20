import streamlit as st

st.session_state.setdefault("threshold", 0.5)
st.session_state.setdefault("show_labels", True)
st.session_state.setdefault("history", [])
st.session_state.setdefault("last_result", None)


def render():
    ct, cs = st.columns([4, 1])
    with ct:
        st.markdown(
            "<h2 style='margin:0;color:#111'>Home</h2>",
            unsafe_allow_html=True)
        st.caption(
            "Welcome to AeroVision — Real-time Drone Detection System")
    with cs:
        st.markdown("""
        <div style='display:flex;justify-content:flex-end;
                    align-items:center;gap:6px;padding-top:6px'>
            <div style='width:10px;height:10px;border-radius:50%;
                        background:#16a34a'></div>
            <span style='font-size:12px;color:#6b7280'>Model Ready</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:6px 0 16px 0'>", unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div style='background:#1a1a2e;border-radius:12px;
                padding:28px 32px;margin-bottom:20px;
                display:flex;justify-content:space-between;
                align-items:center'>
        <div>
            <h1 style='color:white;margin:0;font-size:28px'>
                AeroVision</h1>
            <p style='color:#9ca3af;margin:8px 0 0 0;font-size:14px'>
                Upload an image and detect drones instantly using
                a trained YOLOv8 deep learning model.
            </p>
        </div>
        <div style='font-size:52px;opacity:0.3'>🛸</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶  Start Detection", type="primary"):
        st.switch_page("pages/upload.py")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Feature cards
    c1, c2, c3 = st.columns(3, gap="medium")
    for col, icon, title, sub in [
        (c1, "📤", "Upload Image",
         "JPG, JPEG, PNG · up to 10 MB"),
        (c2, "🔍", "Auto Detection",
         "YOLOv8 bounding boxes & confidence"),
        (c3, "📊", "Instant Results",
         "Annotated image + stats in seconds"),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:#1e1e30;border:1px solid #2d2d45;
                        border-radius:10px;padding:20px;min-height:120px'>
                <div style='font-size:24px;margin-bottom:10px'>{icon}</div>
                <div style='font-weight:700;font-size:14px;color:white;
                            margin-bottom:4px'>{title}</div>
                <div style='font-size:13px;color:#9ca3af'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # How it works
    st.markdown("""
    <div style='background:#1e1e30;border:1px solid #2d2d45;
                border-radius:10px;padding:20px 24px 16px 24px'>
        <div style='font-weight:700;font-size:15px;color:white;
                    margin-bottom:16px'>How It Works</div>
    """, unsafe_allow_html=True)

    for col, num, title, sub in zip(
        st.columns(4, gap="medium"),
        ["1", "2", "3", "4"],
        ["Upload Image", "Validate",
         "Detect", "Results"],
        ["Select JPG / PNG", "Format & size check",
         "YOLOv8 inference", "Boxes + confidence"]
    ):
        with col:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;
                        margin-bottom:8px'>
                <div style='min-width:32px;height:32px;border-radius:50%;
                            background:#DC2626;color:white;font-weight:700;
                            display:flex;align-items:center;
                            justify-content:center'>{num}</div>
                <div>
                    <div style='font-weight:600;font-size:13px;
                                color:white'>{title}</div>
                    <div style='font-size:11px;color:#9ca3af'>{sub}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Info strip
    for col, label, val in zip(
        st.columns(4, gap="medium"),
        ["Framework", "Interface", "Dataset", "Output"],
        ["YOLOv8 (Ultralytics)", "Streamlit",
         "Drone Detection — Kaggle",
         "Bounding boxes + Confidence"]
    ):
        with col:
            st.markdown(f"""
            <div style='background:#1e1e30;border:1px solid #2d2d45;
                        border-radius:8px;padding:14px 16px'>
                <div style='font-size:11px;color:#6b7280'>{label}</div>
                <div style='font-weight:700;font-size:13px;
                            color:white;margin-top:4px'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center;font-size:12px;color:#6b7280;"
        "margin-top:16px'>AeroVision &nbsp;|&nbsp; "
        "Dept. of Information Technology &nbsp;|&nbsp; IUB</div>",
        unsafe_allow_html=True)

render()