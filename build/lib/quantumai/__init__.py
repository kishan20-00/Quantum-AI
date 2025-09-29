from client import QuantumAI
from models import Message, ChatCompletionRequest, ChatCompletionResponse
from .exceptions import (
    LLMClientError, AuthenticationError, RateLimitError,
    ServiceUnavailableError, InvalidRequestError
)

__version__ = "0.1.0"
__all__ = [
    "QuantumAI",
    "Message",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "LLMClientError",
    "AuthenticationError",
    "RateLimitError",
    "ServiceUnavailableError",
    "InvalidRequestError"
]