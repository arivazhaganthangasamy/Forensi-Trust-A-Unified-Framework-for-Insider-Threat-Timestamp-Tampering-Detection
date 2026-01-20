import cv2
import threading
import time

class Camera:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        t = threading.Thread(target=self.update, daemon=True)
        t.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            time.sleep(0.01)

    def get_frame(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def stop(self):
        self.running = False
        self.cap.release()
