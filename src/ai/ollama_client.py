"""Ollama client for local AI integration"""

from typing import Any, Dict, Optional

import requests

from ..core.config import Config
from ..utils.logger import logger


class OllamaClient:
    """Client for interacting with Ollama API"""

    def __init__(self, host: Optional[str] = None, model: Optional[str] = None):
        self.host = host or Config.OLLAMA_HOST
        self.model = model or Config.OLLAMA_MODEL
        self.api_url = f"{self.host}/api"

    def is_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def list_models(self) -> list[str]:
        """List available models"""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=5)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Optional[str]:
        """Generate text using Ollama"""

        model = model or self.model

        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        if system:
            payload["system"] = system

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        try:
            logger.debug(f"Generating text with model {model}")
            response = requests.post(f"{self.api_url}/generate", json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama generation failed: {e}")
            return None

    def chat(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Optional[str]:
        """Chat with Ollama using conversation history"""

        model = model or self.model

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            logger.debug(f"Chat with model {model}")
            response = requests.post(f"{self.api_url}/chat", json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()
            message = result.get("message", {})
            return message.get("content", "").strip()

        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama chat failed: {e}")
            return None

    def pull_model(self, model: str) -> bool:
        """Pull/download a model"""
        try:
            logger.info(f"Pulling model {model}...")
            response = requests.post(f"{self.api_url}/pull", json={"name": model}, timeout=600)
            response.raise_for_status()
            logger.info(f"Model {model} pulled successfully")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to pull model {model}: {e}")
            return False
