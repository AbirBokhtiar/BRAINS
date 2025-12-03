# import os
# from typing import Optional
# from langchain_openai import ChatOpenAI

# # Initialize OpenAI LLM via LangChain
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
# OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")  # or gpt-4, gpt-5-mini when available

# _llm_instance = None

# def _get_llm():
#     """Lazy-load LLM instance."""
#     global _llm_instance
#     if _llm_instance is None:
#         if not OPENAI_API_KEY:
#             raise RuntimeError("OPENAI_API_KEY not set in environment")
#         _llm_instance = ChatOpenAI(
#             api_key=OPENAI_API_KEY,
#             model=OPENAI_MODEL,
#             temperature=0.2,
#             max_tokens=512,
#             base_url=OPENAI_API_BASE,
#         )
#     return _llm_instance

# def _stub_response(prompt: str) -> str:
#     """Fallback stub for testing without API key."""
#     return (
#         "[LLM placeholder response]\n"
#         f"Prompt length: {len(prompt)}\n"
#         "Top recommendation: schedule specialized workup.\n"
#     )

# def generate(
#     prompt: str, 
#     max_tokens: int = 512, 
#     temperature: float = 0.2, 
#     system_prompt: Optional[str] = None
# ) -> str:
#     """
#     Generate text using OpenAI via LangChain.
#     - Requires OPENAI_API_KEY in env.
#     - Falls back to stub if API key not set or on error.
#     """
#     if not OPENAI_API_KEY:
#         return _stub_response(prompt)

#     try:
#         llm = _get_llm()
#         # Combine system prompt with user prompt if provided
#         full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
#         response = llm(full_prompt)
#         return response.strip()
#     except Exception as e:
#         print(f"LLM request failed: {str(e)}")
#         return _stub_response(prompt)

# ml-service-python\app\ml_core\llm_connector.py
import os
from typing import Optional
from openai import OpenAI

# ──────────────────────────────────────────
# Environment Variables
# ──────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")  # default model

_client: Optional[OpenAI] = None


# ──────────────────────────────────────────
# Lazy-load OpenAI Client
# ──────────────────────────────────────────
def _get_client() -> OpenAI:
    global _client

    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set in environment variables.")

        _client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    return _client


# ──────────────────────────────────────────
# Fallback Response (No API Key or Error)
# ──────────────────────────────────────────
def _stub_response(prompt: str) -> str:
    return (
        "[LLM placeholder response]\n"
        f"Prompt length: {len(prompt)} characters\n"
        "Top recommendation: Further clinical evaluation required.\n"
    )


# ──────────────────────────────────────────
# Main Generation Function
# ──────────────────────────────────────────
def generate(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.2,
    system_prompt: Optional[str] = None,
) -> str:

    # If no API key → fallback mode
    if not OPENAI_API_KEY:
        return _stub_response(prompt)

    try:
        client = _get_client()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return completion.choices[0].message["content"].strip()

    except Exception as e:
        print(f"[LLM Error] {e}")
        return _stub_response(prompt)
