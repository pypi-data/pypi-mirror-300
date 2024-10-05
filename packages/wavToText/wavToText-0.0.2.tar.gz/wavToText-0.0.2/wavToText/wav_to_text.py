import os
import sys
import wave
import deepspeech
import numpy as np
from scipy.signal import resample

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from test_env import check_python_version



class AudioText:
    model_path = config.models['pbmm']
    scorer_path = config.models['scorer']

    def __init__(self, wav_file: str):
        if not os.path.isfile(wav_file):
            raise ValueError("The specified wav file does not exist.")
        self.wav_file = wav_file

        self.model = deepspeech.Model(self.model_path)
        self.model.enableExternalScorer(self.scorer_path)


    def read_wav_file(self):
        with wave.open(self.wav_file, 'rb') as wf:
            channels = wf.getnchannels()
            frames = wf.getnframes()
            buffer = wf.readframes(frames)
            rate = wf.getframerate()
            return buffer, rate, channels
        
    @staticmethod
    def resample_audio(audio, original_rate, target_rate=config.deep_speech_rate):
        """Resample audio to target sample rate (16kHz)."""
        if original_rate != target_rate:
            print(f"Resampling from {original_rate} Hz to {target_rate} Hz...")
            duration = len(audio) / original_rate
            num_samples = int(duration * target_rate)
            audio = resample(audio, num_samples)
        return audio
    
    @staticmethod
    def convert_to_mono(audio, channels):
        """Convert stereo audio to mono if necessary."""
        if channels == 2:
            print("Converting stereo to mono...")
            audio = audio.reshape((-1, 2))
            audio = audio.mean(axis=1)
        return audio
    

    def run(self):
        check_python_version()

        try:
            buffer, rate, channels = self.read_wav_file()
        except Exception as e:
            print(f"Error reading WAV file: {e}")
            return None

        audio = np.frombuffer(buffer, dtype=np.int16)
        audio = AudioText.convert_to_mono(audio, channels)

        if rate != config.deep_speech_rate:
            audio = AudioText.resample_audio(audio, rate)

        audio = audio.astype(np.int16)
        text = self.model.stt(audio)
        return text
    


if __name__ == "__main__":
    audio_file = r'wav_files/2.wav'
    obj = AudioText(audio_file)
    print(obj.run())