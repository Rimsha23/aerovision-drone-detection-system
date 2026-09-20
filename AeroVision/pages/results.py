import streamlit as st
import io


def render():
    ct, cs = st.columns([4, 1])
    with ct:
        st.markdown(
            "<h2 style='margin:0;color:#111'>Detection Results</h2>",
            unsafe_allow_html=True)
    with cs:
        st.markdown("""
        <div style='display:flex;justify-content:flex-end;
                    align-items:center;gap:6px;padding-top:6px'>
            <div style='width:10px;height:10px;border-radius:50%;
                        background:#16a34a'></div>
            <span style='font-size:12px;color:#6b7280'>Model Ready</span>
        </div>""", unsafe_allow_html=True)

    result = st.session_state.get("last_result")
    if result:
        st.caption(f"{result['filename']} • {result['timestamp']}")

    st.markdown("<hr style='margin:6px 0 20px 0'>", unsafe_allow_html=True)

    if not result:
        st.warning("No detection result yet. Go to Upload & Detect first.")
        if st.button("Go to Upload & Detect", type="primary"):
            st.switch_page("pages/upload.py")
        return

    # Summary cards
    drone_count = result["drone_count"]
    avg_conf    = (f"{result['avg_confidence']*100:.1f}%"
                   if drone_count > 0 else "—")
    img_size    = (f"{result['image_original'].width}"
                   f"×{result['image_original'].height}")

    m1, m2, m3, m4 = st.columns(4, gap="medium")
    for col, label, value, color in [
        (m1, "Drones Detected", str(drone_count), "#DC2626"),
        (m2, "Avg Confidence",  avg_conf,          "#ea580c"),
        (m3, "Image Size",      img_size,           "#2563eb"),
        (m4, "Status",          "Complete ✓",       "#16a34a"),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:#1e1e30;border:1px solid #2d2d45;
                        border-radius:10px;padding:16px 20px;
                        margin-bottom:4px'>
                <div style='font-size:12px;color:#9ca3af;
                            margin-bottom:6px'>{label}</div>
                <div style='font-size:24px;font-weight:700;
                            color:{color}'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Images
    img1, img2, tbl = st.columns([2, 2, 1], gap="medium")

    with img1:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:16px'>
            <div style='display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:10px'>
                <span style='font-weight:700;color:white;
                             font-size:14px'>Original Image</span>
                <span style='background:#374151;color:#d1d5db;
                             font-size:11px;padding:2px 10px;
                             border-radius:12px'>ORIGINAL</span>
            </div>
        """, unsafe_allow_html=True)
        st.image(result["image_original"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with img2:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:16px'>
            <div style='display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:10px'>
                <span style='font-weight:700;color:white;
                             font-size:14px'>Detection Output</span>
                <span style='background:#DC2626;color:white;
                             font-size:11px;padding:2px 10px;
                             border-radius:12px'>ANNOTATED</span>
            </div>
        """, unsafe_allow_html=True)
        st.image(result["image_annotated"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tbl:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:16px;min-height:200px'>
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
                            color:white;
                            border-bottom:1px solid #1a1a2e'>
                    <span style='width:36px;color:#6b7280'>
                        #{det['id']}</span>
                    <span style='flex:1'>drone</span>
                    <span style='width:60px;color:#DC2626;
                                 font-weight:700'>
                        {det['confidence']*100:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='color:#6b7280;font-size:13px;margin-top:8px'>"
                "No drones detected in this image.</div>",
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    bar_col, act_col = st.columns(2, gap="medium")

    with bar_col:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:16px'>
            <div style='font-weight:700;color:white;
                        font-size:14px;margin-bottom:14px'>
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

    with act_col:
        st.markdown("""
        <div style='background:#1e1e30;border:1px solid #2d2d45;
                    border-radius:10px;padding:16px'>
            <div style='font-weight:700;color:white;
                        font-size:14px;margin-bottom:14px'>
                Actions</div>
        """, unsafe_allow_html=True)

        img_bytes = io.BytesIO()
        result["image_annotated"].save(
            img_bytes, format="JPEG", quality=95)
        img_bytes.seek(0)

        st.download_button(
            label     = "⬇  Download Result",
            data      = img_bytes,
            file_name = f"annotated_{result['filename']}",
            mime      = "image/jpeg",
            use_container_width=True
        )
        st.markdown(
            "<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("🔍  Detect Another", use_container_width=True):
            st.switch_page("pages/upload.py")

        st.markdown(
            "<div style='font-size:12px;color:#6b7280;margin-top:10px'>"
            "Download saves annotated image to your device.</div>",
            unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.session_state.setdefault("last_result", None)

render()