# Laura v1.0 - Voice-Activated Assistant with Audio Visualization

Laura v1.0 is a voice-activated assistant that performs tasks such as opening and closing applications, adjusting the system volume, and providing real-time audio visualization. The assistant listens for voice commands and executes them while displaying a dynamic circular visualization that responds to ambient sound.

## Features

- **Voice Command Recognition**: 
  - Open and close popular applications like Telegram, Discord, Steam, Epic Games, and Spotify.
  - Adjust system volume with a voice command (e.g., "Set volume to 50%").

- **Audio Visualization**:
  - Real-time circular visualization that reacts to ambient sound.
  - Smooth brightness and radius adjustment based on sound magnitude.

- **Sound Feedback**:
  - Plays a sound when opening or closing an application to confirm the action.

## How It Works

1. **Voice Command Listening**:
   - The assistant uses the `speech_recognition` library to listen for voice commands.
   - Commands are processed and matched against predefined tasks.

2. **Command Execution**:
   - Depending on the recognized command, the assistant can open or close specific applications or adjust the system volume.

3. **Audio Visualization**:
   - The assistant captures audio input and dynamically visualizes it as a circle whose size and color change with the sound magnitude.

4. **Multithreading**:
   - Audio visualization runs on a separate thread, allowing the assistant to process voice commands simultaneously.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries:
  - `numpy`
  - `speech_recognition`
  - `pygame`
  - `sounddevice`
  - `pycaw`
  - `comtypes`
