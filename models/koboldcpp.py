"""
KoboldCpp local LLM via OpenAI-compatible API.

Default Base URL: http://localhost:5001/v1
Chat: POST /v1/chat/completions
Models: GET /v1/models
"""
from .openai_compat import OpenAICompatModel


class KoboldCppModel(OpenAICompatModel):
    """KoboldCpp provider using OpenAI-compatible Chat Completions."""

    DEFAULT_MODEL = ""
    DEFAULT_API_BASE_URL = "http://localhost:5001/v1"
    PROVIDER_DISPLAY_NAME = "KoboldCpp (Local)"
