from app.services.youtube import download_audio_from_youtube
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

url = "https://www.youtube.com/watch?v=t8pPdKYpowI" # Example: "Hello World" in Python
print(f"Testing download for: {url}")

try:
    result = download_audio_from_youtube(url, output_dir="storage/test_downloads")
    print("SUCCESS:")
    print(result)
except Exception as e:
    print("FAILURE:")
    print(e)
