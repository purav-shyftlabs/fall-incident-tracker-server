#!/usr/bin/env python3
"""
Simple run script for the chatbot server.
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("Starting Simple Chatbot API...")
    print(f"Server will run on http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
