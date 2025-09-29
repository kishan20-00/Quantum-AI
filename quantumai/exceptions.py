class LLMClientError(Exception):
    """Base exception for LLM client errors"""
    pass

class AuthenticationError(LLMClientError):
    """Raised when authentication fails"""
    pass

class RateLimitError(LLMClientError):
    """Raised when rate limit is exceeded"""
    pass

class ServiceUnavailableError(LLMClientError):
    """Raised when service is unavailable"""
    pass

class InvalidRequestError(LLMClientError):
    """Raised when request is invalid"""
    pass