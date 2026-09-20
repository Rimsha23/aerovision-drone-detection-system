import streamlit as st

st.set_page_config(page_title="AeroVision", page_icon="🛸", layout="wide")

# Session defaults available across all pages
defaults = {
    "threshold": 0.5,
    "show_labels": True,
    "history": [],
    "last_result": None,
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

home = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
upload = st.Page("pages/upload.py", title="Upload & Detect", icon="📤")
results = st.Page("pages/results.py", title="Results", icon="📊")
history = st.Page("pages/history.py", title="History", icon="🕘")
about = st.Page("pages/about.py", title="About", icon="ℹ️")

pg = st.navigation([home, upload, results, history, about])
pg.run()