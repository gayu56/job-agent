import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL_FAST", "anthropic/claude-3.5-haiku").strip()
DEFAULT_STRONG_MODEL = os.getenv("OPENROUTER_MODEL_STRONG", "anthropic/claude-3.5-sonnet").strip()
FALLBACK_FAST = os.getenv("OPENROUTER_MODEL_FALLBACK_FAST", "").strip()
FALLBACK_STRONG = os.getenv("OPENROUTER_MODEL_FALLBACK_STRONG", "").strip()
MAX_RETRIES = max(1, int(os.getenv("OPENROUTER_MAX_RETRIES", "3")))
RETRY_STATUSES = {429, 502, 503, 504}


class OpenRouterError(RuntimeError):
    """Raised when OpenRouter API invocation fails."""


def _extract_content(payload: dict[str, Any]) -> str:
    try:
        return payload["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError, TypeError) as exc:
        raise OpenRouterError("Malformed OpenRouter response: missing message content.") from exc


def _model_chain(model: str) -> list[str]:
    chain = [model]
    if model == DEFAULT_MODEL and FALLBACK_FAST and FALLBACK_FAST != model:
        chain.append(FALLBACK_FAST)
    if model == DEFAULT_STRONG_MODEL and FALLBACK_STRONG and FALLBACK_STRONG != model:
        chain.append(FALLBACK_STRONG)
    out: list[str] = []
    seen: set[str] = set()
    for m in chain:
        if m and m not in seen:
            seen.add(m)
            out.append(m)
    return out


def call_llm(system_prompt: str, user_prompt: str, model: str = DEFAULT_MODEL) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise OpenRouterError("Missing OPENROUTER_API_KEY. Set it in environment or .env.")

    last_error: str | None = None

    for m in _model_chain(model):
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": m,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    },
                    timeout=120,
                )
            except requests.RequestException as exc:
                last_error = f"OpenRouter network error: {exc}"
                if attempt < MAX_RETRIES - 1:
                    time.sleep(0.35 * (2**attempt))
                    continue
                break

            if response.status_code == 200:
                try:
                    payload = response.json()
                except ValueError as exc:
                    raise OpenRouterError("OpenRouter returned non-JSON response.") from exc
                return _extract_content(payload)

            detail = response.text[:500]
            last_error = f"OpenRouter API error {response.status_code}: {detail}"

            if response.status_code in RETRY_STATUSES and attempt < MAX_RETRIES - 1:
                time.sleep(0.35 * (2**attempt))
                continue

            if response.status_code == 404:
                break

            raise OpenRouterError(last_error)

    raise OpenRouterError(last_error or "OpenRouter request failed.")


def call_llm_strong(system_prompt: str, user_prompt: str) -> str:
    return call_llm(system_prompt, user_prompt, model=DEFAULT_STRONG_MODEL)
