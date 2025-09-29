from abc import ABC, abstractmethod
from typing import Dict, List, Optional, AsyncGenerator, Any
import aiohttp
import requests
from exceptions import (
    AuthenticationError, RateLimitError, ServiceUnavailableError, InvalidRequestError
)

class BaseProvider(ABC):
    @abstractmethod
    def chat_complete(self, messages: List[Dict], **kwargs) -> Dict:
        pass

    @abstractmethod
    async def achat_complete(self, messages: List[Dict], **kwargs) -> Dict:
        pass

    def _handle_errors(self, response: requests.Response) -> None:
        """Handle HTTP errors and raise appropriate exceptions"""
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key or authentication failed")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code == 503:
            raise ServiceUnavailableError("Service temporarily unavailable")
        elif response.status_code >= 400:
            raise InvalidRequestError(
                f"Request failed with status {response.status_code}: {response.text}"
            )