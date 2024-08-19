import numpy as np
import speech_recognition as sr
import subprocess
import os
import signal
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import pygame
import sounddevice as sd
import threading

# Visualization parameters
fs = 44100  # Sampling frequency
chunk_size = 1024  # Buffer size
base_radius = 120  # Base radius of the circle
sensitivity = 30  # Sound sensitivity
color = (0, 153, 255)  # Main color (sky blue)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Laura v1.0')

# Initialize speech recognizer
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Say a command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="en-US")
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand.")
            return None
        except sr.RequestError:
            print("Network error.")
            return None

def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Volume is set in the range from -96.0 to 0.0 dB
    min_vol, max_vol = volume.GetVolumeRange()[:2]
    target_volume = (volume_level / 100) * (max_vol - min_vol) + min_vol
    volume.SetMasterVolumeLevel(target_volume, None)

def play_success_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("open.mp3")
    pygame.mixer.music.play()

def play_close_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("close.mp3")
    pygame.mixer.music.play()

def execute_command(command):
    if command is None:
        return

    if 'open telegram' in command:
        subprocess.Popen([r"C:\Users\User\AppData\Roaming\Telegram Desktop\Telegram.exe"])
        play_success_sound()
    elif 'close telegram' in command:
        close_application('Telegram.exe')

    elif 'open discord' in command:
        subprocess.Popen([r"C:\Users\User\AppData\Local\Discord\Update.exe", "--processStart", "Discord.exe"])
        play_success_sound()
    elif 'close discord' in command:
        close_application('Discord.exe')

    elif 'open steam' in command:
        subprocess.Popen([r"C:\Program Files (x86)\Steam\steam.exe"])
        play_success_sound()
    elif 'close steam' in command:
        close_application('steam.exe')

    elif 'open epic games' in command:
        subprocess.Popen([r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"])
        play_success_sound()
    elif 'close epic games' in command:
        close_application('EpicGamesLauncher.exe')

    elif 'open spotify' in command:
        subprocess.Popen([r"C:\Users\User\AppData\Roaming\Spotify\Spotify.exe"])
        play_success_sound()
    elif 'close spotify' in command:
        close_application('Spotify.exe')

    elif 'set volume to' in command:
        try:
            volume_level = int(command.split('set volume to')[1].strip())
            if 0 <= volume_level <= 100:
                set_volume(volume_level)
                print(f"Volume set to {volume_level}%")
            else:
                print("Please specify a value from 0 to 100.")
        except ValueError:
            print("Could not recognize the volume level.")
    else:
        print("Command not recognized.")

def close_application(process_name):
    try:
        for proc in subprocess.check_output(['tasklist']).splitlines():
            if process_name.encode('utf-8') in proc:
                pid = int(proc.split()[1])
                os.kill(pid, signal.SIGTERM)
                play_close_sound()
                print(f"{process_name.split('.')[0]} closed.")
                break
    except Exception as e:
        print(f"Error closing {process_name.split('.')[0]}: {e}")

# Function to draw a circle with smooth radius and brightness change
def draw_circle(screen, magnitude):
    screen.fill((0, 0, 0))  # Black background
    dynamic_radius = int(base_radius + magnitude * sensitivity)

    # Smooth brightness change limited to 255
    brightness = max(0, min(int((magnitude * 100) % 255), 255))
    dynamic_color = (
        max(0, min(brightness, 255)),
        max(0, min(brightness + 50, 255)),
        max(0, min(brightness + 100, 255))
    )

    pygame.draw.circle(screen, dynamic_color, (300, 300), dynamic_radius)
    pygame.display.flip()

# Function for audio capture and visualization display
def audio_visualization():
    stream = sd.InputStream(samplerate=fs, channels=1, dtype='int16')
    stream.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        data = stream.read(chunk_size)[0]
        data = np.frombuffer(data, dtype=np.int16)
        magnitude = np.abs(data).mean() / 5000

        draw_circle(screen, magnitude)
        clock.tick(60)

    stream.stop()
    pygame.quit()

# Start voice assistant and visualization in parallel
if __name__ == "__main__":
    # Start visualization in a separate thread
    threading.Thread(target=audio_visualization, daemon=True).start()

    # Main assistant loop
    while True:
        command = listen()
        if command:
            execute_command(command)
