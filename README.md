# keyword-detection-tool
This tool detects keywords in real time and triggers any other function to implement into the Companion project.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Usage

```python
from wakeword_detector import WakeWordDetector

# Create the detector
detector = WakeWordDetector(['alexa'], threshold=0.5)

# Define an action
def on_wake(word, score):
    print(f"Detected: {word}")

# Register the action
detector.register_callback('alexa', on_wake)

# Start listening
detector.start()
```

## Modular Structure

```
.
├── wakeword_detector.py   # Main module
├── test_wakeword.py       # Test script
├── requirements.txt       # Dependencies
└── models/               # Folder for custom models (optional)
    └── hey_companion.onnx
```

## Testing

Run the test script:
```bash
python test_wakeword.py
```

## Customization

### Creating a custom model

1. Record audio samples of your phrase
2. Use [openWakeWord training](https://github.com/dscripka/openWakeWord#training-new-models)
3. Place the `.onnx` model in `models/`

### Modifying detection threshold

- `threshold=0.3`: Sensitive (more detections)
- `threshold=0.5`: Balanced (default)
- `threshold=0.7`: Strict (fewer false positives)

## Architecture

The system is designed modularly:

- **WakeWordDetector**: Main class managing detection
- **Callbacks**: Actions triggered upon detections
- **Separate thread**: Non-blocking audio processing
- **Queue**: Thread-safe communication

## Integration Example

```python
# Integration with voice assistant
def activate_assistant(word, score):
    # 1. Play confirmation sound
    play_sound("ding.wav")
    
    # 2. Start STT
    text = speech_to_text()
    
    # 3. Process command
    process_command(text)

detector.register_callback('hey_companion', activate_assistant)
```

## Performance

- CPU usage: ~5-10% on Qualcomm X Plus
- RAM: ~100MB
- Latency: <100ms

## License

GPLv3
