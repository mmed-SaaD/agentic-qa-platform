import requests

from pydantic import BaseModel

class OllamaClient:
    def __init__(
            self,
            base_url: str = "http://localhost:11434",
            model: str = "qwen3:1.7b",
    ):
        self.base_url = base_url.strip("/")
        self.model = model

    def generate(self, prompt: str, output_schema: type[BaseModel] | None = None) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": False,
        }

        if output_schema is not None:
            payload["format"] = output_schema.model_json_schema()

        response = requests.post(
            url,
            json=payload,
            timeout=180,
        )

        response.raise_for_status()

        data = response.json()

        return response.json()["response"]