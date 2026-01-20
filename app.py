import streamlit as st
import pandas as pd

from camera import Camera
import face_module
import emotion
import file_monitor
import keyboard_monitor
from admin_logger import log_event

st.set_page_config(
    page_title="AI Security System",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 AI Multi-Level Security System")
st.markdown("---")

# ---------------- SESSION STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "idle"

if "person_name" not in st.session_state:
    st.session_state.person_name = None

if "emotion" not in st.session_state:
    st.session_state.emotion = None

if "file_activity" not in st.session_state:
    st.session_state.file_activity = None

if "keyboard_speed" not in st.session_state:
    st.session_state.keyboard_speed = None

# ---------------- UI FUNCTIONS ----------------
def show_status(text, color="green"):
    st.markdown(
        f"<h4 style='color:{color}'>{text}</h4>",
        unsafe_allow_html=True
    )

# ---------------- BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start Security System"):
        st.session_state.stage = "face"
        st.rerun()

with col2:
    if st.button("🛡 Admin Panel"):
        df = pd.read_excel("security_log.xlsx")
        st.subheader("📊 Security Logs")
        st.dataframe(df)
        st.download_button(
            "⬇ Download Excel",
            data=df.to_csv(index=False),
            file_name="security_log.csv",
            mime="text/csv"
        )

# ---------------- PIPELINE ----------------
if st.session_state.stage == "face":
    show_status("Face Authentication Running...", "orange")

    camera = Camera(0)
    person = face_module.start_face_security(camera)

    if not person:
        show_status("Unauthorized Face Detected. System Locked.", "red")
        st.stop()

    st.session_state.person_name = person
    show_status(f"Face Authorized ✔ ({person})", "green")

    st.session_state.stage = "emotion"
    st.rerun()

elif st.session_state.stage == "emotion":
    show_status("Emotion Monitoring Active...", "orange")

    em = emotion.start_emotion_monitor(Camera(0))
    st.session_state.emotion = em

    show_status(f"Emotion Detected: {em}", "green")

    st.session_state.stage = "file"
    st.rerun()

elif st.session_state.stage == "file":
    show_status("File Monitoring Active...", "orange")

    fa = file_monitor.start_file_monitor()
    st.session_state.file_activity = fa

    show_status("File Monitoring Completed ✔", "green")

    st.session_state.stage = "keyboard"
    st.rerun()

elif st.session_state.stage == "keyboard":
    show_status("Keyboard Speed Monitoring Active...", "orange")

    ks = keyboard_monitor.start_keyboard_monitor()
    st.session_state.keyboard_speed = ks

    # ---------------- SAVE TO EXCEL ----------------
    log_event(
        st.session_state.person_name,
        st.session_state.emotion,
        st.session_state.file_activity,
        st.session_state.keyboard_speed
    )

    show_status("Security Data Saved Successfully 🔐", "green")
    st.session_state.stage = "idle"
