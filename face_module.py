import cv2
import face_recognition
import ctypes
import time

def lock_system():
    """Lock the Windows system immediately."""
    ctypes.windll.user32.LockWorkStation()

def start_face_security(camera):
    """
    Run face recognition.
    Returns the name of the authorized person if successful, otherwise None.
    """
    # ---------------- KNOWN FACES ----------------
    known_faces = []
    known_names = []

    face_files = ["faces/11.jpg", "faces/12.jpg", "faces/13.jpg"]
    names = ["Arivu", "Virat", "Modi"]

    for file, name in zip(face_files, names):
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_faces.append(encodings[0])
            known_names.append(name)

    print("🔍 Face Authentication Started")

    authorized_name = None

    while True:
        frame = camera.get_frame()
        if frame is None:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)

        face_locations = face_recognition.face_locations(small)
        face_encodings = face_recognition.face_encodings(small, face_locations)

        status_text = "NO FACE"
        color = (255, 255, 0)
        unauthorized_detected = False

        for face in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face)
            if True in matches:
                idx = matches.index(True)
                authorized_name = known_names[idx]
                status_text = f"WELCOME {authorized_name}"
                color = (0, 255, 0)
            else:
                status_text = "UNAUTHORIZED FACE"
                color = (0, 0, 255)
                unauthorized_detected = True

        # Draw status
        cv2.putText(frame, status_text, (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        cv2.imshow("Face Security", frame)
        key = cv2.waitKey(1) & 0xFF

        # ❌ Unauthorized → lock system
        if unauthorized_detected:
            print("❌ Unauthorized Face Detected – Locking System")
            time.sleep(1)
            lock_system()
            cv2.destroyAllWindows()
            return None

        # ✅ Authorized + Q → move next
        if key == ord("q") and authorized_name:
            print(f"✅ Face Authorized ({authorized_name}) – Moving to Next Stage")
            cv2.destroyAllWindows()
            return authorized_name

    cv2.destroyAllWindows()
    return None
