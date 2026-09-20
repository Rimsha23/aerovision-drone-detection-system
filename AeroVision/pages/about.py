import streamlit as st


def render():
    ct, cs = st.columns([4, 1])
    with ct:
        st.markdown(
            "<h2 style='margin:0;color:#111'>About AeroVision</h2>",
            unsafe_allow_html=True)
        st.caption("Project information and system details")
    with cs:
        st.markdown("""
        <div style='display:flex;justify-content:flex-end;
                    align-items:center;gap:6px;padding-top:6px'>
            <div style='width:10px;height:10px;border-radius:50%;
                        background:#16a34a'></div>
            <span style='font-size:12px;color:#6b7280'>Model Ready</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:6px 0 20px 0'>", unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div style='background:#1a1a2e;border:1px solid #2d2d45;
                border-radius:12px;padding:24px 28px;margin-bottom:20px'>
        <div style='display:flex;align-items:center;gap:16px'>
            <div style='width:56px;height:56px;border-radius:50%;
                        border:2px solid #DC2626;display:flex;
                        align-items:center;justify-content:center;
                        font-weight:700;font-size:18px;color:#DC2626'>
                AV</div>
            <div>
                <div style='font-size:22px;font-weight:700;color:white'>
                    AeroVision</div>
                <div style='font-size:13px;color:#9ca3af;
                            margin:4px 0 10px 0'>
                    Drone Detection with Machine Learning</div>
                <span style='background:#2563eb;color:white;
                             font-size:11px;padding:3px 10px;
                             border-radius:12px'>v1.0.0</span>
                <span style='background:#DC2626;color:white;
                             font-size:11px;padding:3px 10px;
                             border-radius:12px;margin-left:6px'>
                    YOLOv8</span>
                <span style='background:#16a34a;color:white;
                             font-size:11px;padding:3px 10px;
                             border-radius:12px;margin-left:6px'>
                    Streamlit</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    card = ("background:#1e1e30;border:1px solid #2d2d45;"
            "border-radius:10px;padding:20px")

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"<div style='{card}'>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-weight:700;font-size:15px;color:white;"
            "margin-bottom:14px'>Project Details</div>",
            unsafe_allow_html=True)
        for lbl, val in [
            ("Title",      "AeroVision: Drone Detection"),
            ("Student",    "Rimsha Malik"),
            ("Roll No",    "F22BINFT1M01062"),
            ("Supervisor", "Dr. Syed Ali Nawaz Shah"),
            ("Dept",       "Information Technology"),
            ("Uni",        "IUB Bahawalpur"),
        ]:
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;"
                f"margin-bottom:8px;font-size:13px'>"
                f"<span style='color:#6b7280'>{lbl}:</span>"
                f"<span style='font-weight:600;color:white'>{val}</span>"
                f"</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div style='{card}'>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-weight:700;font-size:15px;color:white;"
            "margin-bottom:14px'>Technology Stack</div>",
            unsafe_allow_html=True)
        for lbl, val, color in [
            ("Language",  "Python 3.10",             "white"),
            ("Detection", "YOLOv8 (Ultralytics)",    "#60a5fa"),
            ("Interface", "Streamlit",                "#60a5fa"),
            ("CV Lib",    "OpenCV",                   "#60a5fa"),
            ("Training",  "Kaggle Notebooks",         "#60a5fa"),
            ("Dataset",   "Drone Detection (Kaggle)", "#60a5fa"),
        ]:
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;"
                f"margin-bottom:8px;font-size:13px'>"
                f"<span style='color:#6b7280'>{lbl}:</span>"
                f"<span style='font-weight:600;color:{color}'>{val}</span>"
                f"</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div style='{card}'>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-weight:700;font-size:15px;color:white;"
            "margin-bottom:14px'>Model Performance</div>",
            unsafe_allow_html=True)
        for lbl, val, color in [
            ("Architecture", "YOLOv8n",  "white"),
            ("Classes",      "3",        "white"),
            ("mAP@0.5",      "87.3 %",  "#4ade80"),
            ("Precision",    "91.2 %",  "#4ade80"),
            ("Recall",       "84.6 %",  "#fb923c"),
            ("Weights",      "best.pt", "#60a5fa"),
        ]:
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;"
                f"margin-bottom:8px;font-size:13px'>"
                f"<span style='color:#6b7280'>{lbl}:</span>"
                f"<span style='font-weight:600;color:{color}'>{val}</span>"
                f"</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='{card};padding:20px 24px'>
        <div style='font-weight:700;font-size:15px;color:white;
                    margin-bottom:16px'>System Flow</div>
    """, unsafe_allow_html=True)

    for col, num, title, sub in zip(
        st.columns(4, gap="medium"),
        ["1","2","3","4"],
        ["Upload Image","Validate File",
         "Detect Drones","Show Results"],
        ["Select JPG / PNG","Format & size check",
         "YOLOv8 inference","Boxes + confidence"]
    ):
        with col:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px'>
                <div style='min-width:32px;height:32px;border-radius:50%;
                            background:#DC2626;color:white;font-weight:700;
                            display:flex;align-items:center;
                            justify-content:center'>{num}</div>
                <div>
                    <div style='font-weight:600;font-size:13px;
                                color:white'>{title}</div>
                    <div style='font-size:12px;color:#9ca3af'>{sub}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='{card};display:flex;justify-content:space-between;
                align-items:center;padding:14px 20px'>
        <div style='font-size:13px;color:#6b7280'>
            © 2025 AeroVision &nbsp;|&nbsp; Final Year Project
            &nbsp;|&nbsp; Islamia University of Bahawalpur
        </div>
        <a href='#' style='background:#2563eb;color:white;
                           padding:8px 16px;border-radius:8px;
                           font-size:13px;font-weight:600;
                           text-decoration:none'>View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)

render()