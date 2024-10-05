import os
import sys


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

models = {
    'pbmm': os.path.join(BASE_DIR, "models", "deepspeech-0.9.3-models.pbmm"),
    'scorer': os.path.join(BASE_DIR, "models", "deepspeech-0.9.3-models.scorer")
}

deep_speech_rate = 16000

requirements_path = os.path.join(BASE_DIR, 'requirements.txt')