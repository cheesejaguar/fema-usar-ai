from nemollm import NemoLLM

class LLMService:
    """Wrapper around the NeMo LLM client."""

    def __init__(self, api_key: str, model: str):
        self.client = NemoLLM(api_key=api_key)
        self.model = model

    def generate(self, message: str) -> str:
        chat_context = [{"role": "user", "content": message}]
        resp = self.client.generate_chat(model=self.model, chat_context=chat_context)
        try:
            return resp["choices"][0]["message"]["content"]
        except Exception:
            return str(resp)
