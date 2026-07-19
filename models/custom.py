"""
Custom AI model implementation

User-defined local or remote OpenAI-compatible endpoints.
"""
from .openai_compat import OpenAICompatModel


class CustomModel(OpenAICompatModel):
    """
    Custom OpenAI-compatible provider.
    API Key is optional (typical for local servers).
    """

    DEFAULT_MODEL = ""
    DEFAULT_API_BASE_URL = ""
    PROVIDER_DISPLAY_NAME = "Custom"
