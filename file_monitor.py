from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import ctypes
from pynput import keyboard

TARGET_FILE = "file.txt"
USB_DRIVES = ["D:\\", "E:\\", "G:\\", "H:\\", "I:\\"]

def show_popup(msg):
    """Display a Windows popup message."""
    ctypes.windll.user32.MessageBoxW(
        0, msg, "Security Alert", 0x10 | 0x1000
    )

class USBHandler(FileSystemEventHandler):
    """Handles file creation events for monitored USB drives."""
    def __init__(self):
        super().__init__()
        self.activity_log = []

    def on_created(self, event):
        if not event.is_directory and TARGET_FILE in event.src_path:
            time.sleep(0.5)
            msg = f"⚠ Protected file copied:\n{event.src_path}"
            show_popup(msg)
            print(msg)
            self.activity_log.append(event.src_path)

def start_file_monitor():
    """
    Monitor USB drives for TARGET_FILE.
    Returns a summary string of detected file activity.
    """
    print("📂 File Monitoring Started (Press Q to continue)")

    handler = USBHandler()
    observer = Observer()

    # Schedule monitoring on all existing USB drives
    for usb in USB_DRIVES:
        if os.path.exists(usb):
            observer.schedule(handler, usb, recursive=True)

    observer.start()
    stop_flag = False

    def on_press(key):
        nonlocal stop_flag
        if key == keyboard.KeyCode.from_char('q'):
            stop_flag = True
            return False  # stop listener

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while not stop_flag:
            time.sleep(0.2)
    finally:
        observer.stop()
        observer.join()
        listener.stop()

    # Generate summary of activity
    if handler.activity_log:
        summary = f"Protected file copied:\n" + "\n".join(handler.activity_log)
    else:
        summary = "No suspicious file activity detected."

    print("➡ File Monitoring Completed")
    return summary
