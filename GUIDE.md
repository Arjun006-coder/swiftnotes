# Swift Notes iOS App - Hackathon Guide 🍎

## 🚀 Mission
Build **Swift Notes**, a native iOS/macOS app that feels like Apple Notes but has a "Brain". It uses your local VidSage Python backend to process videos into seamless study sessions.

## 📦 Project Structure
This folder (`SwiftNotesiosapp`) is a self-contained package containing:
1.  `SwiftNotes/`: The iOS/macOS App (Xcode Project).
2.  `backend/`: The Python AI Engine (FastAPI + Celery).

---

## 🛠️ Part 1: Setup the AI Backend (On Mac)

Since this app relies on a local AI engine, you need to set up the backend on your Mac first.

### 1. Install System Requirements
*   **Python 3.10+**: Install via [Homebrew](https://brew.sh/) (`brew install python`) or python.org.
*   **FFmpeg**: Required for audio processing.
    ```bash
    brew install ffmpeg
    ```
*   **Ollama**: Required for local LLM (Llama 3).
    1.  Download from [ollama.com](https://ollama.com).
    2.  Run the following command in Terminal to pull the model:
        ```bash
        ollama pull llama3:8b
        ```

### 2. Configure the Backend
Open Terminal and navigate to the `backend` folder inside this package:

```bash
cd path/to/SwiftNotesiosapp/backend
```

Create a virtual environment and install dependencies:

```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Server
You need two terminal tabs running:

**Tab 1: FastAPI (The API)**
```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Note: `--host 0.0.0.0` allows the iOS Simulator/Device to connect to your Mac.*

**Tab 2: Celery (The Worker)**
```bash
source venv/bin/activate
celery -A app.core.celery_app worker --loglevel=info
```

---

## 📱 Part 2: Build the iOS App

### 1. Open the Project
1.  Open **Xcode**.
2.  Open the folder `SwiftNotesiosapp/SwiftNotes`.
3.  Wait for Xcode to index the files.

### 2. Configure Network
Open `ViewModels/APIService.swift`.
*   If running on **iOS Simulator**: `http://localhost:8000` usually works, but `http://127.0.0.1:8000` is safer.
*   If running on **Real iPhone**: Find your Mac's LAN IP (Option+Click WiFi icon -> Copy IP Address). Update `baseURL`:
    ```swift
    private let baseURL = "http://192.168.1.X:8000/api"
    ```

### 3. Run!
Press **Cmd+R** to build and run the app.

---

## 🧪 Testing the Flow
1.  **Upload**: Use the backend/web dashboard to upload a video for now (or implement the upload button in Swift).
2.  **Process**: Watch the "Celery" terminal tab. You should see logs like `Ollama... Transcribing...`.
3.  **View**: Once finished, pull down (refresh) the list in the Swift App. Your new "Smart Note" should appear!

## 💡 Hackathon Tips
*   **Canvas**: The `PKCanvasView` is the "wow" factor. Make sure drawing works smoothly.
*   **Ollama Speed**: If Llama 3 is too slow on your Mac, try `ollama pull llama3:8b` (which is standard) or `gemma:2b` for speed. Update `services/llm_factory.py` if you change models.
