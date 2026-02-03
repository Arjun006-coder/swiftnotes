# VidSage Implementation Plan

## Goal
Build **VidSage**, an AI Video Intelligence Platform designed to transform passive video watching (lectures, webinars) into active, structured study materials (notes, cheat sheets, numericals). The immediate goal is to set up a production-ready **monorepo** structure with a **Next.js frontend** and **FastAPI backend**.

## Architecture & Technology Stack

### Core Strategy
- **Web First (PWA-ready)**: Fastest iteration, easy deployment.
- **Monorepo**: Unified codebase for frontend and backend.

### Frontend (User Interface)
- **Framework**: Next.js (App Router, TypeScript)
- **Styling**: Tailwind CSS + ShadCN/Radix UI
- **State**: Zustand / React Query

### Backend (The Brain)
- **Language**: Python
- **Framework**: FastAPI (Async, ML-friendly)
- **Task Queue**: Celery + Redis (Planned for sync processing)

### AI Pipeline (Conceptual for later phases)
- **Transcription**: Whisper Large v3 (Multilingual)
- **LLM**: GPT-4 family for structuring / LLaMA for cost-optimization
- **Database**: PostgreSQL (Relational) + Pinecone/Qdrant (Vector)

## File Structure (Monorepo)
```
VidSage/
│
├── frontend/        # Next.js web app
├── backend/         # FastAPI + AI pipelines
├── infra/           # Docker, deployment configs
├── docs/            # Architecture, prompts
└── README.md
```

## User Review Required
> [!IMPORTANT]
> **GPU Requirement**: Local execution of Whisper/LLMs requires significant hardware resources. For development, we will mock heavy AI calls or use APIs until the async worker infrastructure is fully established.

## Proposed Changes

### 1. Project Initialization [PHASE 0]
- [x] Create root `VidSage` directory (Already exists as git repo)
- [ ] Initialize `frontend` with `create-next-app`
- [ ] Initialize `backend` with Python `venv` and `FastAPI` structure
- [ ] Setup global `.gitignore`

### 2. Frontend Foundation [PHASE 1]
#### [frontend/](file:///c:/Users/HP/OneDrive/Desktop/VidSage/frontend)
- Setup Next.js with TypeScript and Tailwind.
- Clean up boilerplate.
- Create core folder structure: `components`, `lib`, `hooks`.
- **Note**: Antigravity will be used here later for UI generation.

### 3. Backend Core [PHASE 2 - COMPLETED]
#### [backend/](file:///c:/Users/HP/OneDrive/Desktop/VidSage/backend)
- Setup `venv` and install `fastapi`, `uvicorn`.
- Create `main.py` entry point.
- Define basic directory structure: `api`, `services`, `core`, `models`.
- Create a simple health check endpoint.
- **Async Setup**: Redis + Celery installed and configured.

### 4. Transcription Pipeline [PHASE 3 - COMPLETED]
#### Storage & Services
- Create storage structure (`storage/videos`, `storage/audio`, etc.) and update `.gitignore`.
- Implement `services/audio.py` for FFmpeg extraction.
- Update `services/transcription.py` to return segments (timestamps).
- Implement `services/chunking.py` for semantic chunking.
- Update `tasks/video_tasks.py` to orchestrate Video -> Audio -> Transcript -> Chunking.

### 5. Knowledge Structuring Engine [PHASE 4 - CURRENT]
#### Models & Prompts
- [ ] Create `models/knowledge_schema.py` (Pydantic models for Theory, Formulas, Examples).
- [ ] Create `prompts/knowledge_extraction.txt` (The "Gold" prompt).
#### Services
- [ ] Create `services/llm_factory.py` (Abstraction for LLM calls - OpenAI/others).
- [ ] Create `services/knowledge_extractor.py` (Chunk -> JSON logic).
- [ ] Create `services/knowledge_merger.py` (Deduplication & Normalization).
- [ ] Update `tasks/video_tasks.py` to include Knowledge Extraction step.

### 6. Video Brain & Dashboard [PHASE 5 - CURRENT]
#### Phase 5A: Knowledge Dashboard (Frontend)
- [ ] Backend: Add `GET /knowledge/{video_id}` endpoint.
- [ ] Frontend: Create dynamic route `dashboard/[videoId]`.
- [ ] Frontend: Implement Tabs (Overview, Theory, Formulas, Examples, Cheat Sheet).
- [ ] Frontend: Create specialized components for each tab (Accordion for theory, Math block for formulas).

#### Phase 5B: Q&A Bot (Video Brain)
- [ ] Backend: Implement `search_knowledge` (Keyword overlap).
- [ ] Backend: Create `POST /chat` endpoint.
- [ ] Frontend: Build Chat Interface (Bubbles, Loading state).
- [ ] Prompt: "Closed-book" tutor prompt.

### 7. Integration Verification
- Ensure Frontend starts on localhost:3000.
- Ensure Backend starts on localhost:8000.

## Phase 5B: Video Brain Refinement (Q&A)
- [ ] Backend: Update `chat_service.py` to index full transcripts
- [ ] Backend: Relax LLM Prompt to allow external knowledge ("Open Book")
- [ ] Backend: Implement detailed search over transcript segments


### Automated Checks
- **Frontend Build**: Run `npm run build` in `frontend/` to ensure no TS errors.
- **Backend Startup**: Run `uvicorn app.main:app` and curl the health check endpoint.

### Manual Verification
- Open browser to `http://localhost:3000` to see the Next.js landing page.
- Open browser to `http://localhost:8000/docs` to see FastAPI Swagger UI.

## Phase 6: Real Retrieval (Vector DB / RAG) [NEW]
### Technology
- **Vector Database**: Qdrant (Local via `qdrant-client`).
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (Local, CPU-friendly).
- **Strategy**: Semantic Search over chunks (Theory, Formulas, Examples).

### Schema (Payload)
- `text`: The actual content chunk.
- `type`: "theory" | "formula" | "example".
- `video_id`: UUID.
- `chunk_id`: Integer index.

### Changes
- [ ] Backend: Install `qdrant-client`, `sentence-transformers`.
- [ ] Backend: Create `services/vector_db.py` (Singleton Qdrant client).
- [ ] Backend: Update `process_video` task to Embed & Index chunks after extraction.
- [ ] Backend: Refactor `chat_service.py` to use `vector_search` instead of keyword match.
- [ ] Backend: Impose "Hard Rule" (Low similarity -> "Not covered").

## Phase 7: Functional Enhancements & Polish [NEW]
### 7.1 Better Extraction (Code & Practical)
- **Problem**: Code examples are currently trapped in "theory".
- **Solution**: Add `practical` field to schema for Code Snippets / Real-world scenarios.
- [ ] Backend: Update `knowledge_schema.py`
- [ ] Backend: Update `knowledge_extraction.txt` prompt
- [ ] Frontend: Add "Practical / Code" Tab

### 7.2 Source-Aware Answers
- [ ] Backend: Ensure RAG context includes timestamps.
- [ ] Backend: Prompt LLM to cite timestamps (e.g. "[02:30]").

### 7.3 YouTube Integration
- [ ] Backend: Install `yt-dlp`.
- [ ] Backend: Create `services/youtube.py` to download audio from URL.
- [ ] Frontend: Add "Paste YouTube URL" input to Upload page.

### 7.4 Multilingual Support (Hindi/Hinglish)
- [ ] Backend: Configure Whisper to `task="transcribe"` (Auto-detect language).
- [ ] Backend: Update LLM Prompts to handle mixed-language transcripts.
- [ ] Backend: Add `original_language` field to metadata.

## Phase 8: Supabase Integration (Auth & Database) [NEW]
### Strategy
- **Database**: PostgreSQL (Supabase) for user data and video metadata.
- **Auth**: Supabase Auth (JWT) for secure login/signup.
- **Storage**: Supabase Storage for video and audio files (migrating from local disk).

### Schema (Supabase)
#### `profiles` table
- `id`: uuid (PK, references auth.users)
- `email`: text
- `full_name`: text

#### `videos` table
- `id`: uuid (PK)
- `user_id`: uuid (FK -> profiles.id)
- `title`: text
- `video_url`: text (link to Supabase storage)
- `status`: text (processing, completed, failed)
- `metadata`: jsonb (store transcription summary/subject)

### Steps
- [ ] **Frontend**: Install `@supabase/supabase-js` and `@supabase/ssr`.
- [ ] **Frontend**: Create Auth middleware and Login/Signup pages.
- [ ] **Backend**: Install `supabase` python client.
- [ ] **Backend**: Create a `deps.py` for JWT verification using Supabase public keys.
- [ ] **Backend**: Migrate file-based metadata to PostgreSQL.
- [ ] **Storage**: Update pipeline to upload results to Supabase Buckets.

## Phase 9: Deployment & Final Polish [FUTURE]
- [ ] CI/CD with GitHub Actions.
- [ ] Deployment to Vercel (Frontend) and Railway/Render (Backend).





