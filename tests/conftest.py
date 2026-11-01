import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Keep chromadb from sending anonymous usage telemetry during tests.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import pytest


class FakeNemoLLM:
    """Stand-in for the NVIDIA NeMo LLM client (a paid third-party network API).

    Records every ``generate_chat`` call so tests can check the request the
    application builds, and returns a configurable response payload.
    """

    instances = []
    response = None

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.calls = []
        FakeNemoLLM.instances.append(self)

    def generate_chat(self, model, chat_context):
        self.calls.append({"model": model, "chat_context": chat_context})
        if FakeNemoLLM.response is not None:
            return FakeNemoLLM.response
        return {"choices": [{"message": {"role": "assistant", "content": f"reply:{chat_context[-1]['content']}"}}]}


@pytest.fixture
def fake_nemo(monkeypatch):
    import services.llm_service as llm_service

    FakeNemoLLM.instances = []
    FakeNemoLLM.response = None
    monkeypatch.setattr(llm_service, "NemoLLM", FakeNemoLLM)
    return FakeNemoLLM
