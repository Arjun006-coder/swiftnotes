import os
import yt_dlp
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_audio_from_youtube(url: str, output_dir: str = "storage/videos") -> dict:
    """
    Downloads audio from a YouTube URL using yt-dlp.
    Returns metadata dict with 'video_id', 'title', 'file_path'.
    """
    try:
        # Generate a unique video ID
        video_id = str(uuid.uuid4())
        
        # Ensure directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Helper to get info without downloading first
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                original_id = info.get('id', 'unknown')
            except Exception as e:
                logger.error(f"Failed to fetch video info: {e}")
                raise ValueError("Invalid YouTube URL or video unavailable.")

        # Configure download options
        # We download audio only to save bandwidth/space, as we primarily need transcript
        # But for "Video Player" we technically need the Video too if we want to show it?
        # The user said "working on yt link instead of video uploading manually".
        # If we only download audio, we can't play the video in the dashboard easily unless we play the YouTube embed.
        # Implementation Detail: 
        # Option A: Download Video+Audio (Heavy).
        # Option B: Download Audio for processing, and use YouTube Embed Player in Frontend.
        # Option C: Download Video (Medium quality).
        
        # Given "VidSage" transforms passive watching to active study, having the video is good.
        # But storing many YouTube videos locally is heavy.
        # However, the current `VideoPlayer` expects a local file `src`.
        # Let's download the generated video (worst case format "bestvideo+bestaudio" or just "mp4").
        # For speed/MVP, let's download a decent mp4 (720p or similar).
        
        output_template = os.path.join(output_dir, f"{video_id}.%(ext)s")
        
        # Simpler options to avoid complex format selection issues
        ydl_opts = {
            'format': 'best', # best audio+video available
            'outtmpl': output_template,
            'quiet': False, # Enable output to see errors in logs
            'no_warnings': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading YouTube video: {url}")
            ydl.download([url])
            
        # Verify file exists
        # yt-dlp might append extension based on format (e.g. .mp4, .mkv, .webm)
        files = os.listdir(output_dir)
        downloaded_file = None
        
        # Strict prefix matching might fail if yt-dlp sanitizes characters in ID (unlikely for UUID)
        # But let's look for the file carefully.
        for f in files:
            # Check if file starts with video_id AND is a video file
            if f.startswith(video_id) and f.lower().endswith(('.mp4', '.mkv', '.webm', '.flv', '.avi', '.mov', '.m4a', '.webm')):
                downloaded_file = os.path.join(output_dir, f)
                break
        
        if not downloaded_file:
             # Fallback: sometimes yt-dlp puts it in a temp file or similar?
             # List directory content for debugging
             logger.error(f"Files in storage: {files}")
             raise FileNotFoundError(f"Download completed but file not found for ID: {video_id}")
        
        if not downloaded_file:
            raise FileNotFoundError("Download failed, file not found.")
            
        return {
            "video_id": video_id,
            "title": title,
            "file_path": downloaded_file,
            "original_url": url,
            "duration": duration,
            "youtube_id": original_id
        }

    except Exception as e:
        logger.error(f"YouTube Download Error: {e}")
        raise e
