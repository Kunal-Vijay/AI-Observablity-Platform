from __future__ import annotations

from examples.reference_runtime.llm import OpenRouterClient


def test_byok_pins_google_ai_studio_and_skips_model_fallbacks() -> None:
    client = OpenRouterClient(
        "sk-test",
        "google/gemma-4-26b-a4b-it:free",
        fallbacks=("openai/gpt-oss-20b:free",),
        byok_providers=("google-ai-studio",),
    )
    payload = client._build_payload("hi", json_mode=True)
    assert payload["provider"] == {"only": ["google-ai-studio"]}
    assert "models" not in payload
    assert payload["response_format"] == {"type": "json_object"}


def test_without_byok_sends_model_fallbacks() -> None:
    client = OpenRouterClient(
        "sk-test",
        "google/gemma-4-26b-a4b-it:free",
        fallbacks=("openai/gpt-oss-20b:free",),
    )
    payload = client._build_payload("hi")
    assert "provider" not in payload
    assert payload["models"] == ["openai/gpt-oss-20b:free"]
