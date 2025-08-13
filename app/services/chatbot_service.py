import re
from typing import List, Optional
from app.services.gemini_service import gemini_service
from app.services.database_service import database_service
from app.models.chat import ChatHistory
from app.config import settings

class ChatbotService:
    """Simple chatbot service"""
    
    def __init__(self):
        self._database_data = None
        self._is_initialized = False
    
    def _extract_sql_query(self, text: str) -> Optional[str]:
        """Extract SQL query from AI response"""
        # Look for SQL queries in code blocks
        sql_patterns = [
            r'```sql\s*(.*?)\s*```',
            r'```\s*(SELECT.*?)\s*```',
            r'SELECT\s+.*?(?:;|$)',
        ]
        
        for pattern in sql_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sql_query = match.group(1).strip()
                sql_query = re.sub(r'^sql\s*', '', sql_query, flags=re.IGNORECASE)
                return sql_query
        
        return None

    def _format_query_results(self, results: dict) -> str:
        """Format query results for display"""
        if not results.get("success"):
            return f"Query Error: {results.get('error', 'Unknown error')}"
        
        data = results.get("data", [])
        row_count = results.get("row_count", 0)
        columns = results.get("columns", [])
        
        if row_count == 0:
            return "Query executed successfully. No results found."
        
        # Create simple table
        table = "| " + " | ".join(columns) + " |\n"
        table += "| " + " | ".join(["---"] * len(columns)) + " |\n"
        
        # Add data rows (limit to first 20 rows)
        for i, row in enumerate(data[:20]):
            table += "| " + " | ".join([str(row.get(col, "")) for col in columns]) + " |\n"
        
        if row_count > 20:
            table += f"\n... and {row_count - 20} more rows"
        
        return f"Query Results ({row_count} rows):\n\n{table}"
    
    async def initialize(self) -> str:
        """Initialize the chatbot"""
        if self._is_initialized:
            return "Chatbot is ready!"
        
        try:
            # Get database data
            dataframes = await database_service.fetch_all_tables_data()
            self._database_data = database_service.dataframes_to_csv_string(dataframes)
            
            # Get database schema
            schema_data = await database_service.get_database_schema()
            
            # Set data in Gemini service
            gemini_service.set_database_data(self._database_data, schema_data)
            
            self._is_initialized = True
            return "Chatbot is ready!"
            
        except Exception as e:
            return f"Failed to initialize: {str(e)}"
    
    async def send_message(self, user_message: str, history: Optional[List] = None) -> str:
        """Send a message to the chatbot"""
        try:
            # Initialize if not done
            if not self._is_initialized:
                await self.initialize()
            
            # Convert history to Gemini format
            gemini_history = []
            if history:
                gemini_history = gemini_service.convert_messages_to_gemini_format(history)
            
            # Add user message
            gemini_history.append(ChatHistory(
                role="user",
                parts=[{"text": user_message}]
            ))
            
            # Get response from Gemini
            response = await gemini_service.generate_response(gemini_history)
            print("THE REPSPOSNE FROM THE GOOGLE",response)
            # Check if response contains SQL query
            sql_query = self._extract_sql_query(response)
            
            if sql_query:
                # Execute the SQL query
                query_results = await database_service.execute_sql_query(sql_query)
                results_text = self._format_query_results(query_results)
                return results_text
            
            return response
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def is_initialized(self) -> bool:
        """Check if chatbot is initialized"""
        return self._is_initialized
    
    def get_config(self) -> dict:
        """Get chatbot configuration"""
        return {
            "name": settings.CHATBOT_NAME,
            "description": settings.CHATBOT_DESCRIPTION
        }
    
    async def reload_data(self) -> str:
        """Reload the data"""
        try:
            dataframes = await database_service.fetch_all_tables_data()
            self._database_data = database_service.dataframes_to_csv_string(dataframes)
            
            schema_data = await database_service.get_database_schema()
            gemini_service.set_database_data(self._database_data, schema_data)
            
            return "Data reloaded successfully."
            
        except Exception as e:
            return f"Failed to reload data: {str(e)}"

# Create service instance
chatbot_service = ChatbotService()
