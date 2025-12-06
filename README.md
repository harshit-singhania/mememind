# MemeMind

**MemeMind** is an AI-powered platform that automatically generates memes from your daily photos, moods, and events.

## Repository Structure

- **`app-mobile/`**: React Native / Flutter mobile application (Coming Soon).
- **`services/api/`**: FastAPI backend service.
    - Uses **Python 3.11** and **FastAPI**.
    - Managed via `requirements.txt` (pip).
- **`infra/`**: Infrastructure configuration (Terraform, Cloud Run info).
- **`ci/`**: Continuous Integration scripts.

## Getting Started

### Backend API

To run the backend locally:

1.  Navigate to the API service:
    ```bash
    cd services/api
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the server:
    ```bash
    uvicorn app.main:app --reload
    ```
   
See [services/api/README.md](services/api/README.md) for more details.

## Features (Planned)
- **Moment Detector**: Extracts tags and vibe from photos.
- **Humor Engine**: Generates witty captions using LLMs.
- **Template Stylist**: Auto-formats memes.
- **Reel Composer**: Assembles short video reels.
