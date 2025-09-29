import requests
import aiohttp
import json
from typing import Dict, List, Optional, AsyncGenerator, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from providers.base import BaseProvider
from exceptions import RateLimitError, ServiceUnavailableError
from constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, MAX_RETRIES

class CustomProvider(BaseProvider):
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        default_model: Optional[str] = "default",
        additional_headers: Optional[Dict[str, str]] = None,
        timeout: int = DEFAULT_TIMEOUT
    ):
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_BASE_URL
        self.default_model = default_model
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "LLM-Client/1.0.0"
        }
        
        if additional_headers:
            self.headers.update(additional_headers)

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, ServiceUnavailableError))
    )
    def chat_complete(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Send chat completion request to custom endpoint"""
        
        url = f"{self.base_url}/chat/completions"
        model = model or self.default_model
        
        payload = {
            "messages": messages,
            "model": model,
            **kwargs
        }
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            
            self._handle_errors(response)
            return response.json()
            
        except requests.exceptions.Timeout:
            raise ServiceUnavailableError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise ServiceUnavailableError("Connection error")
        except json.JSONDecodeError:
            raise InvalidRequestError("Invalid JSON response from server")

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, ServiceUnavailableError))
    )
    async def achat_complete(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Async version of chat_complete"""
        
        url = f"{self.base_url}/chat/completions"
        model = model or self.default_model
        
        payload = {
            "messages": messages,
            "model": model,
            **kwargs
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    
                    if response.status != 200:
                        self._handle_errors_async(response)
                    
                    return await response.json()
                    
        except aiohttp.ClientTimeout:
            raise ServiceUnavailableError("Request timeout")
        except aiohttp.ClientConnectionError:
            raise ServiceUnavailableError("Connection error")

    def _handle_errors_async(self, response: aiohttp.ClientResponse) -> None:
        """Handle errors for async requests"""
        if response.status == 401:
            raise AuthenticationError("Invalid API key or authentication failed")
        elif response.status == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status == 503:
            raise ServiceUnavailableError("Service temporarily unavailable")
        elif response.status >= 400:
            raise InvalidRequestError(
                f"Request failed with status {response.status}"
            )

    def stream_chat(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        **kwargs
    ) -> Generator[Dict, None, None]:
        """Stream chat completion responses"""
        url = f"{self.base_url}/chat/completions"
        model = model or self.default_model
        
        payload = {
            "messages": messages,
            "model": model,
            "stream": True,
            **kwargs
        }
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
                stream=True
            )
            
            self._handle_errors(response)
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        line = line[6:]
                        if line.strip() == '[DONE]':
                            break
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.Timeout:
            raise ServiceUnavailableError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise ServiceUnavailableError("Connection error")