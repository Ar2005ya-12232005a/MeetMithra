from .config import settings


def get_llm(model: str | None = None, temperature: float = 0):
    provider = settings.llm_provider.lower()
    model = model or settings.llm_model

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=model,
            temperature=temperature,
            api_key=settings.groq_api_key or None,
            timeout=90,
            max_retries=3,
        )
    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=settings.google_api_key or None,
            timeout=90,
            max_retries=3,
        )
    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")