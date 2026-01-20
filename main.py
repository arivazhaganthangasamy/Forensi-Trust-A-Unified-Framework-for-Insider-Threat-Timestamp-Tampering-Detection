from camera import Camera
import face_module
import emotion
import file_monitor
import keyboard_monitor

def main():
    camera = Camera(0)

    print("🔐 Security System Started")

    # ---------------- FACE AUTH ----------------
    face_ok = face_module.start_face_security(camera)

    if not face_ok:
        print("❌ Unauthorized Face – System Stopped")
        return

    input("Press ENTER or Q in window to continue to Emotion Monitoring...")

    # ---------------- EMOTION ----------------
    emotion.start_emotion_monitor(camera)
    input("Press ENTER or Q in window to continue to File Monitoring...")

    # ---------------- FILE MONITOR ----------------
    file_monitor.start_file_monitor()
    input("Press ENTER or Q in window to continue to Keyboard Monitor...")

    # ---------------- KEYBOARD SPEED ----------------
    keyboard_monitor.start_keyboard_monitor()

if __name__ == "__main__":
    main()
