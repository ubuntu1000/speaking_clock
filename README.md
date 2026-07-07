# Speaking Clock

A cross-platform speaking clock application with a GUI that announces the time using text-to-speech. Built with Python, tkinter, and Microsoft Edge TTS.

## Features

- **Real-time clock display** - Shows current time, date, and period (AM/PM)
- **Automatic hourly announcements** - Optionally speak the time every minute
- **Manual speech** - Click "Speak Now" to hear the current time
- **Multiple voices** - Choose from 5 different voice options (US, GB, AU accents)
- **Adjustable speech rate** - Control playback speed from -50% to +50%
- **Cross-platform support** - Works on Linux, macOS, and Windows
- **Error handling** - Graceful error messages for network or TTS issues

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Internet connection (for Microsoft Edge TTS service)

## Installation

### Linux/macOS

1. Clone the repository:
   ```bash
   git clone https://github.com/ubuntu1000/speaking_clock.git
   cd speaking_clock
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install edge-tts
   ```

3. Ensure audio playback is available:
   - **Linux**: `aplay` (usually included) or install `alsa-utils`
   - **macOS**: `afplay` (built-in)

### Windows

1. Clone the repository:
   ```bash
   git clone https://github.com/ubuntu1000/speaking_clock.git
   cd speaking_clock
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or:
   ```bash
   pip install edge-tts
   ```

3. Ensure PowerShell is available (built-in on Windows)

## Usage

Run the application:
```bash
python speaking_clock.py
```

### Controls

- **Voice** - Select from available voices (Aria, Guy, Jenny, Sonia, Natasha)
- **Rate** - Adjust speech speed (-50%, -25%, +0%, +25%, +50%)
- **Start Speaking** - Toggle automatic time announcements every minute
- **Speak Now** - Manually announce the current time
- **Status** - Shows current state (Stopped, Speaking, Announcing, or Error)

## Architecture

The application consists of:

- **GUI Component** (`SpeakingClockGUI`) - Manages the tkinter interface and user interactions
- **TTS Engine** (`speak()` function) - Handles text-to-speech synthesis using edge-tts
- **Audio Player** (`play_audio()` function) - Cross-platform audio playback
- **Speaking Loop** (`_speak_loop()`) - Background thread that monitors time and triggers announcements

## Troubleshooting

### Audio not playing
- **Linux**: Ensure `aplay` is installed (`apt-get install alsa-utils`)
- **macOS**: Check system audio settings
- **Windows**: Verify PowerShell is available and system audio works

### "Error: Network error" or TTS failures
- Check your internet connection
- Ensure the Microsoft Edge TTS service is accessible from your region
- Try again in a few moments

### ImportError for edge-tts
The application automatically attempts to install `edge-tts` on first run. If installation fails with "externally-managed-environment" error, use:
```bash
pip install --break-system-packages edge-tts
```

## License

MIT

## Contributing

Feel free to submit issues and pull requests!
