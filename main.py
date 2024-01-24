import os
import wave
import time
import threading
import tkinter as tk 
import pyaudio

class VoiceRec:

# gui layout
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(text="🎤", font=("Arial", 110, "bold"),
                                command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()
    
    # click handler function
    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="purple")
            threading.Thread(target=self.record).start()

    # record function
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                            input=True, frames_per_buffer=1024)
        frames = []

        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            sec = passed % 60
            min = passed // 60
            hour = min // 60

            self.label.config(text=f"{int(hour):02d}:{int(min):02d}:{int(sec):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1
        while exists:
            if os.path.exists(f"recording{1}.wav"):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f"recording{i}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

VoiceRec()
