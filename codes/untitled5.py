import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
from playsound import playsound
import time


class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")

        # Buttons
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording, width=20)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED, width=20)
        self.stop_button.pack(pady=10)

        # Variables
        self.is_recording = False
        self.fs = 44100  # Sample rate
        self.filename = "output.wav"  # Default output filename

    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

        
    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Recording Saved", f"Recording saved as {self.filename}")
        time.sleep(2)  # Delay to ensure the file is fully written
        self.play_audio()  # Play audio after recording finishes


    def record_audio(self):
        audio_data = []
        try:
            def callback(indata, frames, time, status):
                if self.is_recording:
                    audio_data.append(indata.copy())
                else:
                    raise sd.CallbackStop

            # Start recording with the callback
            with sd.InputStream(callback=callback, channels=1, samplerate=self.fs):
                while self.is_recording:
                    pass

            # Combine all chunks into a single NumPy array
            audio_array = np.concatenate(audio_data, axis=0)

            # Save the audio data as a WAV file
            write(self.filename, self.fs, (audio_array * 32767).astype(np.int16))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def play_audio(self):
        try:
            playsound(self.filename)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while playing the audio: {e}")


# Main Tkinter loop
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()
