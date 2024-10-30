import aiohttp
from typing import Dict, Any, List
from pynions.core import Plugin

class SerperWebSearch(Plugin):
    """Plugin for fetching SERP data using Serper.dev API"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
        if not self.api_key:
            raise ValueError("Serper API key is required")
        
        self.base_url = "https://google.serper.dev/search"
    
    async def execute(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch SERP results for a given query
        
        Args:
            input_data: Dict containing 'query' key
        Returns:
            List of search results
        """
        query = input_data.get('query')
        if not query:
            raise ValueError("Query is required")
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': 10  # Get top 10 results
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"Serper API error: {response.status}")
                
                data = await response.json()
                
                # Extract organic results
                results = []
                for result in data.get('organic', []):
                    results.append({
                        'title': result.get('title'),
                        'link': result.get('link'),
                        'snippet': result.get('snippet'),
                        'position': result.get('position')
                    })
                
                return results
    
    def validate_config(self) -> bool:
        """Validate plugin configuration"""
        return bool(self.api_key)