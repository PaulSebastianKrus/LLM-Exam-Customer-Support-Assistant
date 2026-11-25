from __future__ import annotations

from collections.abc import Sequence

import requests


class OllamaError(RuntimeError):
    """Raised when the local Ollama service cannot complete a request."""


class OllamaClient:
    def __init__(self, base_url: str, timeout_seconds: int = 180) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _post(self, path: str, payload: dict) -> dict:
        try:
            response = requests.post(
                f"{self.base_url}{path}",
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise OllamaError(
                f"Ollama request failed at {self.base_url}. "
                "Check that Ollama is running and the configured models are installed."
            ) from exc

    def embed(self, model: str, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        try:
            data = self._post("/api/embed", {"model": model, "input": list(texts)})
            embeddings = data.get("embeddings")
            if embeddings:
                return embeddings
        except OllamaError:
            # Older Ollama versions expose only the single-input endpoint.
            pass

        embeddings: list[list[float]] = []
        for text in texts:
            data = self._post("/api/embeddings", {"model": model, "prompt": text})
            embedding = data.get("embedding")
            if not embedding:
                raise OllamaError("Ollama returned no embedding data.")
            embeddings.append(embedding)
        return embeddings

    def chat(self, model: str, system_prompt: str, user_prompt: str) -> str:
        data = self._post(
            "/api/chat",
            {
                "model": model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "options": {"temperature": 0.2},
            },
        )
        content = data.get("message", {}).get("content")
        if not content:
            raise OllamaError("Ollama returned an empty chat response.")
        return content.strip()
