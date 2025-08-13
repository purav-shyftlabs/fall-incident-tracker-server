#!/usr/bin/env python3
"""
Test script for the Healthcare Analytics Chatbot API.
"""

import asyncio
import httpx
import json
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def test_health(self) -> Dict[str, Any]:
        """Test health endpoint."""
        print("Testing health endpoint...")
        try:
            response = await self.client.get(f"{self.base_url}/health")
            print(f"Health Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Health test failed: {e}")
            return {"error": str(e)}
    
    async def test_config(self) -> Dict[str, Any]:
        """Test config validation."""
        print("\nTesting config validation...")
        try:
            response = await self.client.get(f"{self.base_url}/health/config")
            print(f"Config Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Config test failed: {e}")
            return {"error": str(e)}
    
    async def test_chatbot_config(self) -> Dict[str, Any]:
        """Test chatbot configuration endpoint."""
        print("\nTesting chatbot config...")
        try:
            response = await self.client.get(f"{self.base_url}/chat/config")
            print(f"Chatbot Config Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Chatbot config test failed: {e}")
            return {"error": str(e)}
    
    async def test_chatbot_status(self) -> Dict[str, Any]:
        """Test chatbot status endpoint."""
        print("\nTesting chatbot status...")
        try:
            response = await self.client.get(f"{self.base_url}/chat/status")
            print(f"Chatbot Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Chatbot status test failed: {e}")
            return {"error": str(e)}
    
    async def test_initialize(self) -> Dict[str, Any]:
        """Test chatbot initialization."""
        print("\nTesting chatbot initialization...")
        try:
            payload = {"session_id": "test_session_123"}
            response = await self.client.post(
                f"{self.base_url}/chat/initialize",
                json=payload
            )
            print(f"Initialize Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Initialize test failed: {e}")
            return {"error": str(e)}
    
    async def test_send_message(self, message: str = "Hello, can you help me with healthcare analytics?") -> Dict[str, Any]:
        """Test sending a message to the chatbot."""
        print(f"\nTesting send message: '{message}'")
        try:
            payload = {
                "message": message,
                "session_id": "test_session_123",
                "history": []
            }
            response = await self.client.post(
                f"{self.base_url}/chat/send",
                json=payload
            )
            print(f"Send Message Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Send message test failed: {e}")
            return {"error": str(e)}
    
    async def run_all_tests(self):
        """Run all API tests."""
        print("Starting API Tests...")
        print("=" * 50)
        
        # Test basic endpoints
        await self.test_health()
        await self.test_config()
        await self.test_chatbot_config()
        await self.test_chatbot_status()
        
        # Test chat functionality
        init_result = await self.test_initialize()
        
        if init_result.get("success"):
            await self.test_send_message()
            await self.test_send_message("Show me the latest trends in our healthcare data")
        else:
            print("Skipping message tests due to initialization failure")
        
        print("\n" + "=" * 50)
        print("API Tests completed!")
        
        await self.client.aclose()

async def main():
    """Main test function."""
    tester = APITester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
