import asyncio
import datetime
import os
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import ttk

try:
    import edge_tts
except ImportError:
    print("Installing edge-tts...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    except subprocess.CalledProcessError:
        # Newer Debian/Ubuntu ("externally-managed-environment") needs this flag
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "edge-tts"]
        )
    import edge_tts

VOICES = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-US-JennyNeural",
    "en-GB-SoniaNeural",
    "en-AU-NatashaNeural",
]
RATES = ["-50%", "-25%", "+0%", "+25%", "+50%"]


def play_audio(filepath):
    if sys.platform == "linux":
        subprocess.run(["aplay", filepath], capture_output=True)
    elif sys.platform == "darwin":
        subprocess.run(["afplay", filepath], capture_output=True)
    else:
        subprocess.run(
            [
                "powershell",
                "-c",
                f'(New-Object Media.SoundPlayer "{filepath}").PlaySync()',
            ],
            capture_output=True,
        )


def speak(text, voice, rate, on_error=None):
    """Generate TTS audio and play it. Runs its own asyncio event loop
    since edge_tts.Communicate.save() is a coroutine, not sync."""
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp = f.name
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        asyncio.run(communicate.save(tmp))
        play_audio(tmp)
    except Exception as exc:  # noqa: BLE001 - surface any TTS/network error to the UI
        if on_error:
            on_error(str(exc))
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)


class SpeakingClockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speaking Clock")
        self.root.geometry("400x360")
        self.root.resizable(False, False)

        self.speaking = False
        self.thread = None
        self.last_spoken_minute = None  # (hour, minute) tuple to avoid double/missed announcements

        self._build_ui()

    def _build_ui(self):
        time_frame = tk.Frame(self.root, bg="#1a1a2e")
        time_frame.pack(fill="x", padx=10, pady=10)

        self.time_label = tk.Label(
            time_frame, font=("Consolas", 48), fg="#00ff88", bg="#1a1a2e"
        )
        self.time_label.pack(pady=10)

        self.date_label = tk.Label(
            time_frame, font=("Arial", 14), fg="#cccccc", bg="#1a1a2e"
        )
        self.date_label.pack()

        ctrl_frame = tk.LabelFrame(self.root, text="Controls", padx=10, pady=10)
        ctrl_frame.pack(fill="x", padx=10, pady=5)

        row1 = tk.Frame(ctrl_frame)
        row1.pack(fill="x", pady=2)
        tk.Label(row1, text="Voice:").pack(side="left")
        self.voice_var = tk.StringVar(value=VOICES[0])
        ttk.Combobox(
            row1, textvariable=self.voice_var, values=VOICES, state="readonly", width=25
        ).pack(side="right")

        row2 = tk.Frame(ctrl_frame)
        row2.pack(fill="x", pady=2)
        tk.Label(row2, text="Rate:").pack(side="left")
        self.rate_var = tk.StringVar(value=RATES[2])
        ttk.Combobox(
            row2, textvariable=self.rate_var, values=RATES, state="readonly", width=25
        ).pack(side="right")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(
            btn_frame,
            text="Start Speaking",
            width=15,
            bg="#00aa55",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.toggle_speaking,
        )
        self.start_btn.pack(side="left", padx=5)

        self.speak_now_btn = tk.Button(
            btn_frame,
            text="Speak Now",
            width=12,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            command=self.speak_now,
        )
        self.speak_now_btn.pack(side="left", padx=5)

        self.status_label = tk.Label(
            self.root, text="Stopped", fg="red", font=("Arial", 10)
        )
        self.status_label.pack()

        self._update_clock()

    def _update_clock(self):
        now = datetime.datetime.now()
        hour = now.hour % 12 or 12
        minute = now.minute
        second = now.second
        period = "AM" if now.hour < 12 else "PM"

        self.time_label.config(text=f"{hour}:{minute:02d}:{second:02d} {period}")
        self.date_label.config(text=now.strftime("%A, %B %d, %Y"))
        self.root.after(500, self._update_clock)

    # -- thread-safe status helpers -------------------------------------
    def _set_status(self, text, color):
        self.root.after(0, lambda: self.status_label.config(text=text, fg=color))

    def _report_error(self, message):
        # Truncate long network/library error messages so the label stays readable
        short = message if len(message) < 60 else message[:57] + "..."
        self._set_status(f"Error: {short}", "orange")

    @staticmethod
    def _build_time_text(now):
        hour = now.hour % 12 or 12
        minute = now.minute
        period = "AM" if now.hour < 12 else "PM"
        if minute > 0:
            return f"{hour} {minute:02d} {period}"
        return f"{hour} {period}"

    def toggle_speaking(self):
        if self.speaking:
            self.speaking = False
            self.start_btn.config(text="Start Speaking", bg="#00aa55")
            self.status_label.config(text="Stopped", fg="red")
        else:
            self.speaking = True
            self.last_spoken_minute = None
            self.start_btn.config(text="Stop Speaking", bg="#cc3333")
            self.status_label.config(text="Speaking every minute", fg="green")
            self.thread = threading.Thread(target=self._speak_loop, daemon=True)
            self.thread.start()

    def _speak_loop(self):
        import time as _time

        while self.speaking:
            now = datetime.datetime.now()
            current_minute = (now.hour, now.minute)
            if now.second == 0 and current_minute != self.last_spoken_minute:
                self.last_spoken_minute = current_minute
                self._speak_time(now)
            _time.sleep(0.5)

    def _speak_time(self, now):
        text = self._build_time_text(now)
        voice = self.voice_var.get()
        rate = self.rate_var.get()
        self._set_status(f"Announcing: {text}", "green" if self.speaking else "blue")
        threading.Thread(
            target=speak, args=(text, voice, rate, self._report_error), daemon=True
        ).start()

    def speak_now(self):
        now = datetime.datetime.now()
        text = self._build_time_text(now)
        voice = self.voice_var.get()
        rate = self.rate_var.get()
        self._set_status(f"Speaking: {text}", "blue")
        threading.Thread(
            target=speak, args=(text, voice, rate, self._report_error), daemon=True
        ).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeakingClockGUI(root)
    root.mainloop()
