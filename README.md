# MemeMind 🧠✨

**MemeMind** is an intelligent, AI-powered meme generator that transforms your photos into hilarious, shareable memes in seconds. By leveraging the power of Google's Gemini Flash for vision and text generation, combined with professional image processing, MemeMind turns everyday moments into viral content.

![MemeMind Demo](https://via.placeholder.com/800x400.png?text=MemeMind+Demo+Banner)

## 🚀 Features

- **📸 Instant Upload**: Seamlessly upload photos from your mobile device or camera.
- **🤖 Advanced AI Vision**: Uses **Google Gemini 1.5 Flash** to analyze image context, objects, facial expressions, and mood.
- **💬 Smart Captioning**: The humor engine generates witty, context-aware captions tailored to the image's vibe.
- **🎨 Pro-Grade Styling**: Automatically formats memes with industry-standard impact fonts, smart text wrapping, and clean layouts.
- **📱 Native Mobile Experience**: Built with **React Native (Expo)** for a smooth experience on iOS and Android.
- **⚡ Asynchronous Processing**: Robust backend worker queue ensures fast and reliable generation.
- **📤 One-Tap Sharing**: Share your creations directly to WhatsApp, Instagram, and other social platforms.
- **🎬 Reel Composer (Video Memes)**: Generates dynamic MP4 video memes with Ken Burns zoom effects, neural text-to-speech voiceovers, and overlaid text.

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **AI Model**: Google Gemini 1.5 Flash
- **Database**: PostgreSQL (via Supabase)
- **ORM**: Prisma Client Python
- **Image Processing**: Pillow (PIL)
- **Video Processing**: MoviePy (with ffmpeg)
- **Text-to-Speech**: Edge-TTS (Neural) / gTTS (Fallback)
- **Storage**: Supabase Storage / Local Fallback

### Mobile App
- **Framework**: React Native with Expo
- **Language**: JavaScript/React
- **State Management**: Zustand
- **Networking**: Axios

## 📂 Project Structure

```bash
mememind/
├── services/api/          # Python FastAPI Backend
│   ├── app/
│   │   ├── agents/        # AI Logic (Vision, Humor, Styling)
│   │   ├── routes/        # API Endpoints
│   │   ├── services/      # Cloud integrations (Supabase)
│   │   └── worker.py      # Background Job Processor
│   ├── prisma/            # Database Schema
│   └── static/            # Local storage for dev
├── app-mobile/            # React Native Mobile App
│   └── src/
│       ├── screens/       # UI Screens
│       ├── api/           # API Client
│       └── store/         # Global State
└── start_dev.sh           # One-click Development Script
```

## 🏁 Getting Started

### Prerequisites

- **Python 3.10+** installed
- **Node.js 18+** installed
- **PostgreSQL** database (Local or Supabase)
- **Google Cloud API Key** (for Gemini)

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
# Database Connection
DATABASE_URL="postgresql://user:password@localhost:5432/mememind"
DIRECT_URL="postgresql://user:password@localhost:5432/mememind"

# Google AI
GOOGLE_API_KEY="your_gemini_api_key_here"

# (Optional) Supabase Storage
SUPABASE_URL="your_supabase_url"
SUPABASE_SERVICE_KEY="your_service_key"
```

### 2. Backend Installation

```bash
cd services/api
pip install -r requirements.txt
prisma generate
prisma db push  # Push schema to DB
```

### 3. Mobile App Installation

```bash
cd app-mobile
npm install
```

## 🏃‍♂️ Running the Project

We provide a convenient script to start all services (Backend API, Worker, and Mobile Bundle) simultaneously:

```bash
./start_dev.sh
```

**Alternatively, run services manually:**

*Terminal 1: Backend API*
```bash
cd services/api
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

*Terminal 2: Background Worker*
```bash
cd services/api
python3 -m app.worker
```

*Terminal 3: Mobile App*
```bash
cd app-mobile
npx expo start
```

## 🧪 Development & Testing

- **Backend Logs**: The worker prints detailed logs for "Detected Moment" and "Generated Captions" to help debug AI responses.
- **Local Storage**: In development, images are saved locally to `services/api/static/uploads` if Supabase credentials are missing.
- **End-to-End Test**: Run `python3 services/api/verify_e2e.py` to test the full pipeline without the mobile app.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License.
