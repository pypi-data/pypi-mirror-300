import requests
from typing import Optional
from .interfaces import PromptResponse

import time

default_ttl = 60  # 60 seconds for caching
cache = {}


class PromptSmith():

    def __init__(self, base_url, api_key, ttl_in_seconds=60):
        """
        :param base_url:
        :param api_key:
        :param ttl_in_seconds:
        """
        self.base_url = base_url
        self.api_key = api_key
        self.ttl_in_seconds = ttl_in_seconds

    def get_prompt(self, unique_key: str) -> Optional[PromptResponse]:
        timestamp_key = f"{unique_key}-timestamp"
        if unique_key in cache and time.time() < cache[timestamp_key] + self.ttl_in_seconds:
            return cache[unique_key]

        url = f"{self.base_url}/api/sdk/prompt/{unique_key}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            cache[unique_key] = result
            cache[timestamp_key] = time.time()
        return None
