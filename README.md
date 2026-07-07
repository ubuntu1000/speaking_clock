# Speaking Clock

A Python-based GUI application that announces the time at regular intervals using text-to-speech (TTS). Perfect for accessibility, background time announcements, or building a talking clock.

## Features

✨ **Key Features:**
- 🎤 Real-time time announcements using Microsoft Edge TTS
- 🎯 Multiple voice options (US, UK, Australian accents)
- 🔊 Adjustable speech rate (+/- 50%)
- 🖥️ Dark-themed GUI with live clock display
- 🔁 Automatic hourly/minute announcements
- 🛑 Manual "Speak Now" button for on-demand announcements
- ⚡ Cross-platform support (Linux, macOS, Windows)
- 🔧 Modular, refactored architecture

## Prerequisites

- **Python 3.9+**
- **Audio playback command:**
  - Linux: `aplay` (alsa-utils)
  - macOS: `afplay` (built-in)
  - Windows: PowerShell with Media.SoundPlayer

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ubuntu1000/speaking_clock.git
cd speaking_clock
```

### 2. Install Dependencies

#### On Linux (Debian/Ubuntu):
```bash
sudo apt-get install alsa-utils python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### On macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

## Project Structure

```
speaking_clock/
├── main.py                 # Application entry point
├── config.py              # Configuration constants
├── audio_player.py        # Audio playback module
├── tts_manager.py         # Text-to-speech logic
├── gui.py                 # GUI components
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Usage

### Starting the Application

```bash
python main.py
```

### GUI Controls

- **Voice Selector**: Choose from 5 different voices
- **Rate Selector**: Adjust speech speed (-50% to +50%)
- **Start Speaking**: Toggle automatic minute announcements
- **Speak Now**: Manually announce the current time
- **Status Display**: Real-time status and error messages

### Available Voices

- `en-US-AriaNeural` - Female US English (default)
- `en-US-GuyNeural` - Male US English
- `en-US-JennyNeural` - Female US English
- `en-GB-SoniaNeural` - Female British English
- `en-AU-NatashaNeural` - Female Australian English

### Speech Rates

- `-50%` - Very slow
- `-25%` - Slow
- `+0%` - Normal (default)
- `+25%` - Fast
- `+50%` - Very fast

## API Reference

### Core Modules

#### `config.py`
Centralized configuration with type hints:
```python
from config import VOICES, RATES, DEFAULT_VOICE, MAX_WORKER_THREADS
```

#### `audio_player.py`
Platform-independent audio playback:
```python
from audio_player import AudioPlayer, AudioPlaybackError

try:
    AudioPlayer.play_audio("path/to/audio.mp3")
except AudioPlaybackError as e:
    print(f"Playback failed: {e}")
```

#### `tts_manager.py`
Text-to-speech management with async support:
```python
from tts_manager import TTSManager

manager = TTSManager()
manager.speak("Hello World", voice="en-US-AriaNeural", rate="+0%")
```

#### `gui.py`
GUI components using Tkinter:
```python
from gui import SpeakingClockGUI
import tkinter as tk

root = tk.Tk()
app = SpeakingClockGUI(root)
root.mainloop()
```

## Troubleshooting

### Issue: "No module named 'edge_tts'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: No sound on Linux
**Solution:** Ensure ALSA is installed and configured
```bash
sudo apt-get install alsa-utils
alsamixer  # Test audio levels
```

### Issue: Application hangs on Windows
**Solution:** Ensure PowerShell is available in PATH. Try:
```powershell
[Environment]::GetEnvironmentVariable("Path", "Machine") | ForEach-Object { $_ -split ';' }
```

### Issue: TTS takes too long
**Solution:** Check internet connection (edge-tts requires online access)

## Error Handling

The application includes comprehensive error handling:
- **Network errors**: Displayed as truncated messages on status label
- **Audio playback failures**: Logged and reported to UI
- **TTS generation errors**: Caught and gracefully handled
- **Thread safety**: Uses thread-safe status updates via `Tk.after()`

## Logging

Enable debug logging by modifying `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Notes

- ✅ Uses thread pool for concurrent TTS generation
- ✅ Non-blocking UI updates with proper thread synchronization
- ✅ Efficient minute tracking to prevent duplicate announcements
- ✅ Automatic cleanup of temporary audio files

## Dependencies

See `requirements.txt`:
- `edge-tts` - Microsoft Edge Text-to-Speech API
- `tkinter` - GUI framework (usually included with Python)

## License

MIT License - feel free to use, modify, and distribute

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Future Enhancements

- 🌙 24-hour mode toggle
- ⏰ Custom announcement intervals
- 🔔 Notification sounds
- 💾 Settings persistence
- 🌐 Multiple language support
- 📱 System tray integration

## Support

For issues, questions, or suggestions, please open an [GitHub Issue](https://github.com/ubuntu1000/speaking_clock/issues).

---

**Made with ❤️ by ubuntu1000**
