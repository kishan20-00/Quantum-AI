from typing import Dict, List, Optional, Generator
from providers.custom import CustomProvider
from utils import validate_api_key, setup_logging
from exceptions import AuthenticationError

class QuantumAI:
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        default_model: Optional[str] = "default",
        additional_headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        debug: bool = False
    ):
        if not validate_api_key(api_key):
            raise AuthenticationError("Invalid API key provided")
        
        if debug:
            setup_logging("DEBUG")
        
        self.provider = CustomProvider(
            api_key=api_key,
            base_url=base_url,
            default_model=default_model,
            additional_headers=additional_headers,
            timeout=timeout
        )

    def chat_complete(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Send chat completion request"""
        return self.provider.chat_complete(messages, model, **kwargs)

    async def achat_complete(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Async chat completion"""
        return await self.provider.achat_complete(messages, model, **kwargs)

    def stream_chat(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        **kwargs
    ) -> Generator[Dict, None, None]:
        """Stream chat responses"""
        return self.provider.stream_chat(messages, model, **kwargs)

    # Additional convenience methods
    def quick_chat(
        self,
        message: str,
        system_message: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """Quick chat with minimal parameters"""
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": message})
        
        response = self.chat_complete(messages, model, **kwargs)
        return response['choices'][0]['message']['content']