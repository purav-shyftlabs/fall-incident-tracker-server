import httpx
from app.config import settings
from app.models.chat import ChatHistory

class GeminiService:
    """Simple Gemini service"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={self.api_key}"
        self._system_prompt = None
    
    def set_database_data(self, database_data: str, schema_data: str = None):
        """Set database data for system prompt"""
        self._system_prompt = self.create_system_prompt(database_data, schema_data)
    
    def create_system_prompt(self, sheet_data: str, schema_data: str = None) -> str:
        """Create system prompt"""
        prompt_parts = [
            "You are a healthcare analytics assistant. Analyze the data and provide insights.",
            "",
            "When asked for data analysis, provide PostgreSQL SQL queries in this format:",
            "while wriing the query make sure to add double quotes around the column names with uppercase letters in alias also, if you are using any function or column name with uppercase letters, make sure to add double quotes around it",
            "if ask for both query and text response, please return the query and text response in the same response AS BELOW FORMAT",
            "if ask any one of them leave one of them empty",
            "if query and text is there do not include any result just return the query and text response in the same response AS BELOW FORMAT",
            "DONT EXECUTE THE QUERY AT ALL"

            "```sql",
            "YOUR_QUERY_HERE",
            "```",
            "```TEXT",
            "YOUR_TEXT_RESPONSE_HERE",
            "```",
            "",
            "Use quotes around column names with uppercase letters.",
            "Example: Use \"RNAO_ASSESSMENT\" instead of RNAO_ASSESSMENT",
            ""
        ]
        
        if schema_data:
            prompt_parts.extend([
                "DATABASE SCHEMA:",
                schema_data,
                ""
            ])
        
        prompt_parts.extend([
            "DATA:",
            sheet_data,
            "",
            "Provide direct, clear responses with actionable insights."
        ])
        
        return "\n".join(prompt_parts)
    
    async def generate_response(self, history: list) -> str:
        """Generate response from Gemini API"""
        # Add system prompt if available
        if self._system_prompt:
            system_history = [ChatHistory(
                role="user",
                parts=[{"text": self._system_prompt}]
            )]
            system_history.append(ChatHistory(
                role="model", 
                parts=[{"text": "I understand. I'm ready to help."}]
            ))
            system_history.extend(history)
            history = system_history
        
        payload = {"contents": [msg.dict() for msg in history]}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
                    
                    if text:
                        return text
                    else:
                        return "Sorry, I couldn't generate a response."
                else:
                    return f"API error: {response.status_code}"
                    
        except Exception as e:
            return f"Error: {str(e)}"
    
    def convert_messages_to_gemini_format(self, messages: list) -> list:
        """Convert messages to Gemini format"""
        gemini_messages = []
        
        for msg in messages:
            if hasattr(msg, 'is_user'):
                role = "user" if msg.is_user else "model"
                text = msg.text
            else:
                role = "user" if msg.get("is_user", False) else "model"
                text = msg.get("text", "")
            
            gemini_messages.append(ChatHistory(
                role=role,
                parts=[{"text": text}]
            ))
        
        return gemini_messages

# Create service instance
gemini_service = GeminiService()
