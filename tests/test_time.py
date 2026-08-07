import sys
import os
import datetime

# Ensure repo root is on sys.path so tests can import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import SpeakingClockGUI


def test_build_time_text_on_the_hour():
    now = datetime.datetime(2026, 1, 1, 15, 0)
    assert SpeakingClockGUI._build_time_text(now) == "It's 3 PM"


def test_build_time_text_with_minutes_pm():
    now = datetime.datetime(2026, 1, 1, 15, 5)
    assert SpeakingClockGUI._build_time_text(now) == "It's 3:05 PM"


def test_build_time_text_midnight():
    now = datetime.datetime(2026, 1, 1, 0, 0)
    assert SpeakingClockGUI._build_time_text(now) == "It's 12 AM"


def test_build_time_text_noon():
    now = datetime.datetime(2026, 1, 1, 12, 0)
    assert SpeakingClockGUI._build_time_text(now) == "It's 12 PM"
