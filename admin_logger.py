import pandas as pd
import os
from datetime import datetime

FILE = "security_log.xlsx"

def log_event(person, emotion, file_activity, keyboard_speed):
    data = {
        "Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Person": [person],
        "Emotion": [emotion],
        "File Activity": [file_activity],
        "Keyboard Speed": [keyboard_speed]
    }

    df_new = pd.DataFrame(data)

    if os.path.exists(FILE):
        df_old = pd.read_excel(FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(FILE, index=False)
