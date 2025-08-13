# Simple Chatbot Server

A simple FastAPI server for a healthcare chatbot.

## What it does

- Connects to a PostgreSQL database
- Uses Google Gemini AI to answer questions
- Provides a chat interface for healthcare data analysis

## How to run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
GEMINI_API_KEY=your_gemini_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=healthcare
DB_USER=postgres
DB_PASSWORD=your_password
```

3. Run the server:
```bash
python run.py
```

The server will start on http://localhost:8000

## API Endpoints

- `GET /` - Server info
- `GET /health` - Health check
- `POST /chat/initialize` - Start chatbot
- `POST /chat/send` - Send message
- `GET /chat/status` - Check chatbot status
- `GET /database/schema` - Get database schema
- `POST /database/execute-query` - Run SQL query

## Files

- `main.py` - Main FastAPI app
- `config.py` - Settings
- `models/` - Data models
- `api/` - API endpoints
- `services/` - Business logic
- `run.py` - Server startup script
