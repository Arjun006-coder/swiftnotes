# Tasks: VidSage Project Setup

## Phase 0: Foundations & Project Structure
- [ ] Create root-level `.gitignore`
- [ ] Create `infra` and `docs` folders

## Phase 1: Frontend Initialization (Next.js)
- [x] Run `npx create-next-app@latest frontend` (TypeScript, Tailwind, App Router)
- [x] Cleanup default Next.js boilerplate
- [x] Create folder structure: `components`, `lib`, `hooks`
- [ ] Verify Frontend runs locally

## Phase 2: Backend Initialization (FastAPI)
- [x] Create `backend` directory
- [x] Setup Python virtual environment (`venv`)
- [x] Install dependencies (`fastapi`, `uvicorn`)
- [ ] Create `backend` structure: `app`, `api`, `services`, `core`
- [ ] Implement `main.py` with health check
- [x] Verify Backend runs locally

## Phase 3: Video -> Transcript Pipeline (Current)
- [x] create `storage/` directory structure and update `.gitignore`
- [x] Update `api/upload.py` to save files locally
- [x] Verify FFmpeg installation (Local binary found)
- [x] Create `services/audio.py` (FFmpeg wrapper)
- [x] Update `services/transcription.py` (Whisper segments)
- [x] Create `services/chunking.py` (Semantic chunking)
- [x] Update `tasks/video_tasks.py` (Full pipeline)
- [x] Manual Verification: Upload video -> Check generated files

## Phase 4: Knowledge Structuring Engine (Current)
- [x] Create `models/knowledge_schema.py` (Pydantic)
- [x] Create `prompts/knowledge_extraction.txt`
- [x] Setup `services/llm_factory.py` (OpenAI/Mock)
- [x] Create `services/knowledge_extractor.py`
- [x] Create `services/knowledge_merger.py`
- [x] Integrate into `tasks/video_tasks.py`
- [x] Manual Verification: Check `storage/knowledge/*.json` (Verified Mock Output)

## Phase 5A: Knowledge Dashboard (Current)
- [x] Backend: Create `GET /api/knowledge/{video_id}` endpoint
- [x] Frontend: Define Knowledge Types in `types.ts`
- [x] Frontend: Create `lib/getVideoKnowledge.ts` fetcher
- [x] Frontend: Create route `app/dashboard/[videoId]/page.tsx`
- [x] Frontend: Implement `tabs/Theory.tsx` (Accordion)
- [x] Frontend: Implement `tabs/Formulas.tsx` (Math view)
- [x] Frontend: Implement `tabs/Examples.tsx`
- [x] Frontend: Implement `tabs/CheatSheet.tsx` (Printable view)

## Phase 5B: Video Brain Refinement (Q&A)
- [x] Backend: Update `chat_service.py` to index full transcripts
- [x] Backend: Relax LLM Prompt to allow external knowledge ("Open Book")
- [x] Backend: Implement search over transcript segments

## Phase 5C: Video Listing & Connectivity
- [x] Backend: Add `GET /api/knowledge` to list all processed videos
- [x] Backend: Integrate Local Ollama (`llama3:8b`) via `requests`
- [x] Frontend: Update `dashboard/page.tsx` to fetch and display video grid

## Phase 5D: Interactive Video & Details Tools
- [x] Backend: Serve static files (`/files`) for video playback
- [x] Frontend: Implement `VideoPlayer` component with Canvas Screenshot
- [x] Frontend: Integrate Player into Dashboard / Add "My Notes"

## Phase 6: Real Retrieval (Vector DB / RAG)
- [x] Backend: Install `qdrant-client` & `sentence-transformers`
- [x] Backend: Create `VectorService` (Initialize Qdrant Local)
- [x] Backend: Implement `Index Video` task (Chunk -> Embed -> Upsert)
- [x] Backend: Implement `RAG Search` (Query -> Embed -> Search)
- [x] Backend: Update Chat Logic to use RAG (Prompt Refinement & Hard Rule)
- [x] Refinement: Removed Hard Rule (Open Book Fallback)
- [x] Refinement: Fixed Video Player CORS for Screenshots



## Phase 7: Functional Enhancements & Polish
- [ ] Backend: Add `PracticalScenario` to Knowledge Schema
- [ ] Backend: Update Extraction Prompt for Code Snippets
- [ ] Backend: Update Merger Logic for Practicals
- [ ] Frontend: Create `tabs/Practical.tsx` for Code display
- [ ] Backend: Ensure RAG Search includes Timestamps
- [ ] Frontend: Display Citations in Chat

### 7.3 YouTube & Multilingual
- [ ] Backend: Install `yt-dlp`
- [ ] Backend: Create `YouTubeService`
- [ ] Frontend: Update `VideoInput` for URL support
- [ ] Backend: Refine Prompts for Hindi/Multilingual
## Phase 8: Supabase Integration
- [ ] Setup Supabase Project & Tables
- [ ] Frontend: Implement Auth Flow (Login/Signup)
- [ ] Backend: Security Middleware (JWT Validation)
- [ ] Data: Link Videos to User IDs
- [ ] Storage: Migrate Local Storage to Supabase Buckets
