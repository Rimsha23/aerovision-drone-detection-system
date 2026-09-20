import streamlit as st


def render():
    ct, cs = st.columns([4, 1])
    with ct:
        st.markdown(
            "<h2 style='margin:0;color:#111'>Detection History</h2>",
            unsafe_allow_html=True)
        st.caption("All images analysed in this session")
    with cs:
        st.markdown("""
        <div style='display:flex;justify-content:flex-end;
                    align-items:center;gap:6px;padding-top:6px'>
            <div style='width:10px;height:10px;border-radius:50%;
                        background:#16a34a'></div>
            <span style='font-size:12px;color:#6b7280'>Model Ready</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:6px 0 16px 0'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#422006;border:1px solid #92400e;
                border-radius:8px;padding:10px 16px;
                font-size:13px;color:#fbbf24;margin-bottom:16px'>
        ℹ️ &nbsp;Session-only history —
        records are cleared when the app is closed.
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.get("history", [])

    sc, f1, f2, f3, cl = st.columns([3, 1, 1, 1, 1], gap="small")
    with sc:
        search = st.text_input(
            "Search history",
            placeholder="🔍  Search filename...",
            label_visibility="collapsed"
        )
    with f1:
        all_btn   = st.button("All",         use_container_width=True)
    with f2:
        found_btn = st.button("Drone Found", use_container_width=True,
                              type="primary")
    with f3:
        none_btn  = st.button("No Drone",    use_container_width=True)
    with cl:
        # No st.rerun() after clear
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state["history"] = []

    filtered = list(reversed(history))
    if search:
        filtered = [r for r in filtered
                    if search.lower() in r["filename"].lower()]
    if found_btn:
        filtered = [r for r in filtered if r["drone_count"] > 0]
    elif none_btn:
        filtered = [r for r in filtered if r["drone_count"] == 0]

    if not filtered:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.info("No records yet. Go to Upload & Detect to get started.")
        return

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    h0,h1,h2,h3,h4,h5 = st.columns([0.4,2.2,2,1.4,1.2,1])
    for col, lbl in zip([h0,h1,h2,h3,h4,h5],
                        ["#","Filename","Date & Time",
                         "Result","Confidence","Action"]):
        col.markdown(
            f"<div style='font-size:12px;font-weight:700;"
            f"color:#6b7280;padding-bottom:6px'>{lbl}</div>",
            unsafe_allow_html=True)

    st.markdown(
        "<hr style='margin:0 0 8px 0;border-color:#2d2d45'>",
        unsafe_allow_html=True)

    for i, record in enumerate(filtered):
        c0,c1,c2,c3,c4,c5 = st.columns([0.4,2.2,2,1.4,1.2,1])

        c0.markdown(
            f"<div style='padding-top:8px;font-size:13px;"
            f"color:#9ca3af'><b>{i+1}</b></div>",
            unsafe_allow_html=True)
        c1.markdown(
            f"<div style='font-size:13px;font-weight:600;color:#111;"
            f"padding-top:4px'>{record['filename']}</div>"
            f"<div style='font-size:11px;color:#9ca3af'>Image file</div>",
            unsafe_allow_html=True)
        c2.markdown(
            f"<div style='font-size:13px;color:#6b7280;padding-top:8px'>"
            f"{record['timestamp']}</div>",
            unsafe_allow_html=True)

        if record["drone_count"] > 0:
            c3.markdown("""
            <div style='background:#DC2626;color:white;border-radius:12px;
                        padding:3px 10px;font-size:12px;font-weight:600;
                        display:inline-block;margin-top:6px'>
                Drone Found</div>""", unsafe_allow_html=True)
            c4.markdown(
                f"<div style='font-weight:700;color:#DC2626;padding-top:8px'>"
                f"{record['avg_confidence']*100:.0f}%</div>",
                unsafe_allow_html=True)
        else:
            c3.markdown("""
            <div style='background:#16a34a;color:white;border-radius:12px;
                        padding:3px 10px;font-size:12px;font-weight:600;
                        display:inline-block;margin-top:6px'>
                No Drone</div>""", unsafe_allow_html=True)
            c4.markdown(
                "<div style='color:#16a34a;padding-top:8px'>—</div>",
                unsafe_allow_html=True)

        if c5.button("View", key=f"view_{i}",
                     use_container_width=True):
            st.session_state["last_result"] = record
            st.switch_page("pages/results.py")

        st.markdown(
            "<hr style='margin:6px 0;border-color:#f3f4f6'>",
            unsafe_allow_html=True)

    st.markdown(
        f"<div style='font-size:12px;color:#9ca3af;margin-top:8px'>"
        f"Showing {len(filtered)} record(s) this session</div>",
        unsafe_allow_html=True)

st.session_state.setdefault("history", [])

render()