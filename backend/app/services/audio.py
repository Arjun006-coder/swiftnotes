import subprocess
import os

def extract_audio(video_path: str, audio_path: str):
    """
    Extracts audio from a video file using FFmpeg.
    Requires 'ffmpeg' to be in the system PATH.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    # Determine FFmpeg path
    # 1. Look for 'ffmpeg.exe' in the current directory (project root/backend)
    # 2. Fallback to system 'ffmpeg'
    if os.path.exists("ffmpeg.exe"):
        ffmpeg_cmd = "ffmpeg.exe"
    elif os.path.exists("bin/ffmpeg.exe"):
        ffmpeg_cmd = "bin/ffmpeg.exe"
    else:
        ffmpeg_cmd = "ffmpeg"

    command = [
        ffmpeg_cmd, "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        audio_path
    ]

    try:
        # Run FFmpeg, suppressing standard output/error to keep logs clean
        # Remove stdout/stderr=subprocess.DEVNULL if you need to debug FFmpeg errors
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise RuntimeError("FFmpeg not found. Please install FFmpeg and add it to your system PATH.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed to extract audio: {e}")
