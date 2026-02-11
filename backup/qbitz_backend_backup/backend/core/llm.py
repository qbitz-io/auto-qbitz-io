"""LLM initialization and configuration."""
from langchain_openai import ChatOpenAI
from .config import settings


def get_llm(temperature: float = None) -> ChatOpenAI:
    """Get configured LLM instance."""
    return ChatOpenAI(
        model=settings.openai_model,
        temperature=temperature if temperature is not None else settings.openai_temperature,
        api_key=settings.openai_api_key
    )
