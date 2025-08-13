# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup Environment
```bash
cd server
cp env.example .env
```

### 2. Configure Your API Key
Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
python run.py
```

### 5. Test the API
Open your browser and go to:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Frontend Example**: Open `frontend_example.html` in your browser

## 🐳 Using Docker (Alternative)

### 1. Build and Run with Docker Compose
```bash
docker-compose up --build
```

### 2. Access the Services
- **API**: http://localhost:8000
- **Frontend**: http://localhost:8080

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat/initialize` | Initialize chatbot |
| POST | `/chat/send` | Send message |
| GET | `/chat/config` | Get config |
| GET | `/chat/status` | Get status |
| POST | `/chat/reload` | Reload data |

## 🔧 Configuration

Key environment variables in `.env`:

```env
GEMINI_API_KEY=your_api_key
SHEET_URLS=["url1", "url2"]
ALLOWED_ORIGINS=["http://localhost:3000"]
DEBUG=True
```

## 🧪 Testing

Run the test script:
```bash
python test_api.py
```

## 📁 Project Structure

```
server/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── api/                 # API routes
│   ├── models/              # Pydantic models
│   └── services/            # Business logic
├── requirements.txt         # Dependencies
├── run.py                  # Start script
├── test_api.py             # Tests
├── frontend_example.html   # Demo frontend
└── docker-compose.yml      # Docker setup
```

## 🆘 Troubleshooting

### Common Issues:

1. **Port 8000 in use**: Change port in `.env`
2. **API key error**: Verify your Gemini API key
3. **CORS errors**: Check `ALLOWED_ORIGINS` in `.env`
4. **Sheet access error**: Ensure Google Sheets are public

### Debug Mode:
```env
DEBUG=True
```

## 📚 Next Steps

1. Customize the Google Sheets URLs
2. Modify the chatbot prompt in `gemini_service.py`
3. Add authentication if needed
4. Deploy to production

## 🎯 Example Usage

```bash
# Initialize chatbot
curl -X POST http://localhost:8000/chat/initialize \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test123"}'

# Send message
curl -X POST http://localhost:8000/chat/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me healthcare trends"}'
```

That's it! Your healthcare analytics chatbot API is ready to use! 🎉
