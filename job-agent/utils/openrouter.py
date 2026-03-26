import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL_FAST", "anthropic/claude-3.5-haiku").strip()
DEFAULT_STRONG_MODEL = os.getenv("OPENROUTER_MODEL_STRONG", "anthropic/claude-3.5-sonnet").strip()


class OpenRouterError(RuntimeError):
    """Raised when OpenRouter API invocation fails."""


def _extract_content(payload: dict[str, Any]) -> str:
    try:
        return payload["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError, TypeError) as exc:
        raise OpenRouterError("Malformed OpenRouter response: missing message content.") from exc


def call_llm(system_prompt: str, user_prompt: str, model: str = DEFAULT_MODEL) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise OpenRouterError("Missing OPENROUTER_API_KEY. Set it in environment or .env.")

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=90,
        )
    except requests.RequestException as exc:
        raise OpenRouterError(f"OpenRouter network error: {exc}") from exc

    if response.status_code != 200:
        detail = response.text[:500]
        raise OpenRouterError(f"OpenRouter API error {response.status_code}: {detail}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise OpenRouterError("OpenRouter returned non-JSON response.") from exc

    return _extract_content(payload)


def call_llm_strong(system_prompt: str, user_prompt: str) -> str:
    return call_llm(system_prompt, user_prompt, model=DEFAULT_STRONG_MODEL)
