import whisper
import torch

# Load model once. 
# In production with GPU, strictly control memory usage here.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=DEVICE)

def transcribe_audio(audio_path: str):
    """
    Transcribes the audio file and returns the raw segments with timestamps.
    """
    # result["segments"] contains:
    # {
    #   "id": 0,
    #   "start": 0.0,
    #   "end": 4.5,
    #   "text": "Hello world...",
    #   ...
    # }
    result = model.transcribe(audio_path)
    return result["segments"]
