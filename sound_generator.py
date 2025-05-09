import pygame
import numpy as np
import os
import wave
import struct

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def create_crash_sound():
    """
    Creates a simple crash sound effect
    """
    # Create a crash sound
    sample_rate = 44100
    duration = 0.5  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a noisy crash sound
    crash = np.random.uniform(-0.7, 0.7, (int(sample_rate * duration), 2))
    
    # Add some low frequency rumble
    crash[:, 0] += 0.6 * np.sin(2 * np.pi * 150 * t) * np.exp(-5 * t)
    crash[:, 1] += 0.6 * np.sin(2 * np.pi * 150 * t) * np.exp(-5 * t)
    
    # Normalize
    crash = crash / np.max(np.abs(crash))
    
    # Convert to 16-bit PCM
    crash = (crash * 32767).astype(np.int16)
    
    return crash

def create_point_sound():
    """
    Creates a simple point scoring sound effect
    """
    # Create a point sound
    sample_rate = 44100
    duration = 0.3  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a coin-like sound
    point = np.zeros((int(sample_rate * duration), 2))
    point[:, 0] = 0.5 * np.sin(2 * np.pi * 1000 * t) * np.exp(-10 * t)
    point[:, 1] = 0.5 * np.sin(2 * np.pi * 1600 * t) * np.exp(-10 * t)
    
    # Normalize
    point = point / np.max(np.abs(point))
    
    # Convert to 16-bit PCM
    point = (point * 32767).astype(np.int16)
    
    return point

def create_background_music():
    """
    Creates simple background music
    """
    sample_rate = 44100
    duration = 10.0  # seconds (will loop)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a simple melody
    music = np.zeros((int(sample_rate * duration), 2))
    
    # Base rhythm
    for i in range(10):
        start = int(i * sample_rate)
        end = int((i + 0.5) * sample_rate)
        freq = 220 if i % 2 == 0 else 330
        music[start:end, 0] += 0.3 * np.sin(2 * np.pi * freq * t[0:end-start])
        music[start:end, 1] += 0.3 * np.sin(2 * np.pi * freq * t[0:end-start])
    
    # Add some higher notes
    for i in range(20):
        start = int(i * 0.5 * sample_rate)
        end = int((i * 0.5 + 0.25) * sample_rate)
        freq = 440 if i % 3 == 0 else (550 if i % 3 == 1 else 660)
        music[start:end, 0] += 0.2 * np.sin(2 * np.pi * freq * t[0:end-start])
        music[start:end, 1] += 0.2 * np.sin(2 * np.pi * freq * t[0:end-start])
    
    # Add a bass line
    for i in range(5):
        start = int(i * 2 * sample_rate)
        end = int((i * 2 + 1.5) * sample_rate)
        freq = 110 if i % 2 == 0 else 165
        music[start:end, 0] += 0.4 * np.sin(2 * np.pi * freq * t[0:end-start])
        music[start:end, 1] += 0.4 * np.sin(2 * np.pi * freq * t[0:end-start])
    
    # Normalize
    music = music / np.max(np.abs(music))
    
    # Convert to 16-bit PCM
    music = (music * 32767).astype(np.int16)
    
    return music

def create_life_lost_sound():
    """
    Creates a sound for when a life is lost
    """
    sample_rate = 44100
    duration = 0.4  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a descending tone
    life_lost = np.zeros((int(sample_rate * duration), 2))
    life_lost[:, 0] = 0.5 * np.sin(2 * np.pi * (800 - 600 * t/duration) * t) * np.exp(-3 * t)
    life_lost[:, 1] = 0.5 * np.sin(2 * np.pi * (800 - 600 * t/duration) * t) * np.exp(-3 * t)
    
    # Normalize
    life_lost = life_lost / np.max(np.abs(life_lost))
    
    # Convert to 16-bit PCM
    life_lost = (life_lost * 32767).astype(np.int16)
    
    return life_lost

def save_wav(sound_array, filename, sample_rate=44100):
    """
    Save a numpy array as a WAV file
    """
    with wave.open(filename, 'w') as wav_file:
        # Set parameters
        nchannels = 2
        sampwidth = 2  # 2 bytes for 16-bit audio
        framerate = sample_rate
        nframes = len(sound_array)
        comptype = 'NONE'
        compname = 'not compressed'
        
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        
        # Write frames
        for sample in sound_array:
            wav_file.writeframes(struct.pack('<hh', sample[0], sample[1]))

# Create and save sounds
def generate_sounds():
    os.makedirs(os.path.join('assets', 'sounds'), exist_ok=True)
    
    # Create and save crash sound
    crash_sound = create_crash_sound()
    save_wav(crash_sound, os.path.join('assets', 'sounds', 'crash.wav'))
    
    # Create and save point sound
    point_sound = create_point_sound()
    save_wav(point_sound, os.path.join('assets', 'sounds', 'point.wav'))
    
    # Create and save background music
    background_music = create_background_music()
    save_wav(background_music, os.path.join('assets', 'sounds', 'background_music.wav'))
    
    # Create and save life lost sound
    life_lost_sound = create_life_lost_sound()
    save_wav(life_lost_sound, os.path.join('assets', 'sounds', 'life_lost.wav'))
    
    print("Sound effects generated successfully!")

if __name__ == "__main__":
    generate_sounds()