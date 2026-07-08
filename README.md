# Remote Control YouTube with Hand Gestures

This project uses your webcam and hand gestures to control YouTube playback with keyboard shortcuts.

## What it does

The script detects your hand with MediaPipe and maps simple gestures to common YouTube commands:

- 5 fingers: Play / Pause
- 1 finger: Advance 10 seconds
- 2 fingers: Rewind 10 seconds
- 3 fingers: Next video

## Requirements

Install the dependencies with:

```bash
pip install opencv-python mediapipe pyautogui
```

## How to run

1. Make sure your webcam is connected.
2. Open the project folder.
3. Run:

```bash
python main.py
```

4. Point the camera at your hand and hold a gesture for about 1 second to confirm the action.
5. Press `q` in the camera window to exit.

## Notes

- The script uses your computer's keyboard shortcuts, so it works best while the YouTube video is focused.
- A safe-stop feature is enabled through `pyautogui`.
- The webcam must be available for gesture detection.
