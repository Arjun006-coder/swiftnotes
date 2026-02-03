# Swift Notes App: Implementation Plan

## Goal
Create a native **iOS & macOS Application** called **"Swift Notes"** that replicates the functionality of the VidSage AI Video Tutor. The app will mimic the native **Apple Notes** UI/UX and integrate AI-generated study material with personal note-taking abilities.

> [!WARNING]
> **Windows Limitation**: You are currently on **Windows**. You can view and edit the Swift code I generate, but **you cannot build or run** this iOS app on your current machine. You will need to move the `swiftnotesiosapp` folder to a **Mac** with Xcode installed to compile and test it.

## Architecture: Hybrid Approach
To ensure no features are lost (Whisper, LLM, Vector DB) without rewriting the entire AI stack in Swift/CoreML (which is massive), we will use a **Client-Server** model:
*   **Brain (Backend)**: Existing **FastAPI Python Backend**. It will run locally (or on a server) and handle heaving lifting (Transcribing, Chunking, Vectors).
*   **Face (Frontend)**: **SwiftUI App**. A native replacement for the Next.js website. It communicates with the Backend via REST API.

## File Structure
```
swiftnotesiosapp/
├── SwiftNotes/
│   ├── App/
│   │   ├── SwiftNotesApp.swift    # Entry point
│   │   └── ContentView.swift       # Main Layout (SplitView)
│   ├── Models/
│   │   ├── Note.swift              # Data Model (Personal vs Smart)
│   │   └── VideoKnowledge.swift    # Decodable structs for API responses
│   ├── ViewModels/
│   │   ├── NotesViewModel.swift    # Logic & State
│   │   └── APIClient.swift         # Connects to Python Backend
│   ├── Views/
│   │   ├── Sidebar/                # Folders/Nav
│   │   ├── SmartNote/              # The "VidSage" View
│   │   │   ├── VideoPlayerView.swift
│   │   │   ├── TheoryView.swift
│   │   │   └── FormulaView.swift
│   │   └── PersonalNote/           # Drawing & Writing
│   │       ├── EditorView.swift
│   │       └── CanvasView.swift    # PencilKit Wrapper
│   └── Resources/
│       └── Assets.xcassets
└── README.md
```

## Features & Roadmap

### Phase 1: Project Setup (The Shell)
*   [ ] Create `swiftnotesiosapp` directory structure.
*   [ ] Create basic **SwiftUI** App structure.
*   [ ] Implement **Apple Notes UI**:
    *   `NavigationSplitView` (Sidebar + Content).
    *   List View with search bar.
    *   Paper-texture background / Clean white styling.

### Phase 2: Personal Notes (The "Notes" Part)
*   [ ] Implement **Text Editor**: A rich text experience (using `TextEditor` or `UITextView` wrapper).
*   [ ] Implement **Drawing**: Integrate **PencilKit** (`PKCanvasView`) to allow drawing/handwriting with Apple Pencil (or touch).
*   [ ] **Persistence**: Save notes to local JSON/CoreData/SwiftData.

### Phase 3: "Smart Session" Integration (The AI Part)
*   [ ] **API Client**: Create a Swift service to talk to `http://localhost:8000`.
*   [ ] **Upload Flow**: Custom UI to pick a video -> Send to Backend -> Poll for status.
*   [ ] **Session View**:
    *   When a video is processed, it saves as a "Smart Note".
    *   **Video Player**: Embed `AVPlayer` at the top.
    *   **Knowledge Blocks**: Render Theory/Formulas as native SwiftUI cards below the video.

### Phase 4: Polish & Ecosystem
*   [ ] **Dark Mode**: Ensure full support.
*   [ ] **iPad OS Support**: Leverage larger screen for Split View.
*   [ ] **macOS Support**: Optimized toolbar and window management.

## Technical Details
*   **Language**: Swift 5.9+
*   **UI Framework**: SwiftUI
*   **Networking**: URLSession async/await
*   **Drawing**: PencilKit
*   **Video**: AVKit
