import cv2
from deepface import DeepFace

def start_emotion_monitor(camera):
    """
    Analyze emotions from camera frames.
    Returns the last detected dominant emotion when Q is pressed.
    """
    print("🙂 Emotion Monitoring Started")

    dominant_emotion = "Unknown"

    while True:
        frame = camera.get_frame()
        if frame is None:
            continue

        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False,
                silent=True
            )
            dominant_emotion = result[0]["dominant_emotion"]

            cv2.putText(
                frame,
                f"Emotion: {dominant_emotion}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        except Exception:
            cv2.putText(
                frame,
                "Emotion: Detecting...",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

        cv2.imshow("Emotion Monitor", frame)
        key = cv2.waitKey(1) & 0xFF

        # ✅ Press Q to finish monitoring
        if key == ord("q"):
            print(f"➡ Emotion Monitoring Completed ({dominant_emotion})")
            cv2.destroyAllWindows()
            return dominant_emotion

    cv2.destroyAllWindows()
    return dominant_emotion
