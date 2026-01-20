from pynput import keyboard
from collections import deque
import time
import ctypes

# ---------------- SYSTEM FUNCTIONS ----------------
def lock_system():
    """Lock the Windows system immediately."""
    ctypes.windll.user32.LockWorkStation()

def show_popup(speed):
    """Display a Windows popup alert for abnormal typing speed."""
    ctypes.windll.user32.MessageBoxW(
        0,
        f"⚠ Abnormal Typing Detected!\n\nSpeed: {speed:.2f} keys/sec\n\nSystem will lock now.",
        "Security Alert",
        0x10 | 0x0
    )

# ---------------- KEYBOARD MONITOR ----------------
def start_keyboard_monitor(threshold=30):
    """
    Monitor keyboard typing speed.
    Returns the last measured typing speed.
    Locks the system if speed exceeds threshold.
    Press Q to exit monitoring normally.
    """
    print("⌨ Keyboard Speed Monitoring Started (Press Q to exit)")

    timestamps = deque(maxlen=200)
    last_speed = 0.0
    LOCKED = False

    def on_press(key):
        nonlocal last_speed, LOCKED

        # Exit normally if Q pressed
        if key == keyboard.KeyCode.from_char('q'):
            print("\n➡ Keyboard Monitoring Completed")
            return False  # stop listener

        if LOCKED:
            return False

        now = time.time()
        timestamps.append(now)

        recent = [t for t in timestamps if now - t <= 3]
        last_speed = len(recent) / 3.0

        print(f"\rTyping Speed: {last_speed:.2f} keys/sec", end="")

        # Lock system if speed exceeds threshold
        if last_speed > threshold:
            LOCKED = True
            show_popup(last_speed)
            lock_system()
            return False  # stop listener after lock

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return last_speed
