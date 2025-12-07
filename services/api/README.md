# MemeMind API Service

This is the backend service for MemeMind, built with FastAPI, Prisma, and Supabase.

## Tech Stack
-   **Framework**: FastAPI (Python 3.11)
-   **Database**: Supabase (PostgreSQL)
-   **ORM**: Prisma Client Python
-   **AI**: Google Gemini Pro/Flash
-   **Container**: Docker

## Setup & Run

### 1. Requirements
Ensure you have `pip` installed.

```bash
cd services/api
pip install -r requirements.txt
```

### 2. Environment Variables
Create a root `.env` file (or symlink it) with the following:

```env
DATABASE_URL="postgresql://...?pgbouncer=true"
DIRECT_URL="postgresql://...:5432/..."
SUPABASE_URL="https://..."
SUPABASE_SERVICE_KEY="..."
GOOGLE_API_KEY="..."
```

### 3. Database Migration
Sync your Prisma schema with the remote Supabase DB:

```bash
# Ensure valid DATABASE_URL in environment (or use .env file)
prisma db push
```

### 4. Running the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## Testing

```bash
python -m pytest
```

## Prisma Lifecycle
-   **Generation**: `prisma generate` (Runs automatically in Docker build)
-   **Schema**: Located at `services/api/prisma/schema.prisma`
