import requests
from typing import List, Dict, Optional

class GammaClient:
    """
    Standardized client for interacting with the Polymarket Gamma API.
    """
    BASE_URL = "https://gamma-api.polymarket.com"

    def fetch_active_crypto_events(self, min_volume: float = 10000.0) -> List[Dict]:
        """
        Fetches active markets with a minimum volume threshold.
        """
        endpoint = f"{self.BASE_URL}/markets"
        params = {
            "active": "true",
            "closed": "false",
            "limit": 100
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        markets = response.json()
        return [m for m in markets if float(m.get('volume', 0)) >= min_volume]

    def normalize_probability(self, price: float) -> int:
        """
        Converts Gamma price (0-1) to Matrix index (0-100).
        """
        return int(round(price * 100))
