import time
from typing import Optional

import requests
from requests_threads import AsyncSession

from .interfaces import PromptResponse

default_ttl = 60  # 60 seconds for caching



class PromptSmith():
    _cache = {}

    def __init__(self, base_url, api_key, ttl_in_seconds=default_ttl):
        """
        :param base_url:
        :param api_key:
        :param ttl_in_seconds:
        """
        self.session = requests.Session()
        self.async_session = AsyncSession()
        self.base_url = base_url
        self.api_key = api_key
        self.ttl_in_seconds = ttl_in_seconds

    def _set_cache(self, key, value):
        self._cache[key] = {"value": value, "time": time.time()}

    def _get_cache(self, key):
        if key in self._cache:
            if time.time() - self._cache[key]["time"] < self.ttl_in_seconds:
                return self._cache[key]["value"]
        return None

    def get_prompt(self, unique_key: str) -> Optional[PromptResponse]:
        if self._get_cache(unique_key):
            return self._get_cache(unique_key)

        url = f"{self.base_url}/api/sdk/prompt/{unique_key}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            self._set_cache(unique_key, result)
            return result
        return None

    async def get_prompt_async(self, unique_key: str) -> Optional[PromptResponse]:
        if self._get_cache(unique_key):
            return self._get_cache(unique_key)
        url = f"{self.base_url}/api/sdk/prompt/{unique_key}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = await self.async_session.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            self._set_cache(unique_key, result)
            return result
        return None
