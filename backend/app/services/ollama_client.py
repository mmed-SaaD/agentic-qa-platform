import requests

class OllamaClient:
    def __init__(
            self,
            base_url: str = "http://localhost:11434",
            model: str = "qwen3:1.7b",
    ):
        self.base_url = base_url.strip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": False,
        }

        response = requests.post(
            url,
            json=payload,
            timeout=180,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]