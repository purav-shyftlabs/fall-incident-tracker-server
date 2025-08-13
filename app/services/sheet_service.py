import httpx
import re
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class SheetService:
    """Service for fetching data from Google Sheets."""
    
    def __init__(self, sheet_urls: List[str]):
        self.sheet_urls = sheet_urls
    
    async def fetch_sheet_data(self, url: str) -> str:
        """
        Fetch CSV data from a Google Sheet URL.
        
        Args:
            url: The Google Sheet URL
            
        Returns:
            CSV data as string
            
        Raises:
            Exception: If fetching fails
        """
        try:
            logger.info(f"Fetching data from: {url}")
            
            # Extract the spreadsheet ID and gid from the URL
            sheet_id_match = url.match(r'/d/(.*?)/')
            gid_match = url.match(r'#gid=(\d+)') or url.match(r'gid=(\d+)')
            
            if not sheet_id_match:
                raise Exception("Invalid Google Sheet URL format. Please ensure it contains a spreadsheet ID.")
            
            spreadsheet_id = sheet_id_match.group(1)
            gid = gid_match.group(1) if gid_match else "0"  # Default to first sheet
            
            csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&gid={gid}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(csv_url)
                
                if response.status_code == 200:
                    return response.text
                else:
                    raise Exception(f"Failed to fetch sheet data from {url}. Status: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error fetching sheet data from {url}: {str(e)}")
            raise Exception(f"Could not fetch data from {url}. Please ensure it is a public Google Sheet with the correct gid.")
    
    async def fetch_all_sheet_data(self) -> str:
        """
        Fetch data from all configured Google Sheets and combine them.
        
        Returns:
            Combined CSV data from all sheets
            
        Raises:
            Exception: If any sheet fails to fetch
        """
        try:
            # Fetch data from all sheets concurrently
            tasks = [self.fetch_sheet_data(url) for url in self.sheet_urls]
            all_sheet_data = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check for any exceptions
            errors = []
            valid_data = []
            
            for i, result in enumerate(all_sheet_data):
                if isinstance(result, Exception):
                    errors.append(f"Sheet {i+1}: {str(result)}")
                else:
                    valid_data.append(result)
            
            if errors:
                raise Exception(f"Failed to fetch some sheets: {'; '.join(errors)}")
            
            # Combine all data with separators
            combined_data = "\n\n---SEPARATOR---\n\n".join(valid_data)
            
            logger.info(f"Successfully fetched data from {len(valid_data)} sheets")
            return combined_data
            
        except Exception as e:
            logger.error(f"Error fetching all sheet data: {str(e)}")
            raise
    
    def validate_sheet_urls(self) -> List[str]:
        """
        Validate the format of Google Sheet URLs.
        
        Returns:
            List of valid URLs
            
        Raises:
            Exception: If any URL is invalid
        """
        valid_urls = []
        invalid_urls = []
        
        for url in self.sheet_urls:
            if re.match(r'https://docs\.google\.com/spreadsheets/d/[a-zA-Z0-9_-]+', url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if invalid_urls:
            raise Exception(f"Invalid Google Sheet URLs: {', '.join(invalid_urls)}")
        
        return valid_urls

# Import asyncio for the gather function
import asyncio
