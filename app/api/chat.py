from fastapi import APIRouter
from app.models.chat import (
    ChatRequest, 
    ChatResponse, 
    InitializeRequest, 
    InitializeResponse,
    ChatbotConfig
)
from app.services.chatbot_service import chatbot_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/initialize", response_model=InitializeResponse)
async def initialize_chatbot(request: InitializeRequest):
    """Initialize the chatbot"""
    initial_message = await chatbot_service.initialize()
    
    return InitializeResponse(
        success=True,
        message=initial_message,
        session_id=request.session_id
    )

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to the chatbot"""
    response = await chatbot_service.send_message(
        user_message=request.message,
        history=request.history
    )
    
    return ChatResponse(
        message=response,
        session_id=request.session_id,
        is_data_loaded=chatbot_service.is_initialized()
    )

@router.get("/config", response_model=ChatbotConfig)
async def get_chatbot_config():
    """Get chatbot configuration"""
    config = chatbot_service.get_config()
    return ChatbotConfig(**config)

@router.get("/status")
async def get_chatbot_status():
    """Get chatbot status"""
    return {
        "is_initialized": chatbot_service.is_initialized(),
        "status": "ready" if chatbot_service.is_initialized() else "initializing"
    }

@router.post("/reload")
async def reload_data():
    """Reload the data"""
    message = await chatbot_service.reload_data()
    return {"message": message, "success": True}
