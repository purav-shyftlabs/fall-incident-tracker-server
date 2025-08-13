import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Simple settings for the app"""
    
    # API Key
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Database settings
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "healthcare")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    # Chatbot settings
    CHATBOT_NAME: str = os.getenv("CHATBOT_NAME", "Simple Chatbot")
    CHATBOT_DESCRIPTION: str = os.getenv("CHATBOT_DESCRIPTION", "A simple chatbot")
    
    def get_db_url(self) -> str:
        """Get database URL"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Create settings instance
settings = Settings()
