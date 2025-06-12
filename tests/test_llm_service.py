import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import types
import importlib

# Provide dummy nemollm module so import works
dummy_module = types.ModuleType("nemollm")
dummy_module.NemoLLM = object
sys.modules.setdefault("nemollm", dummy_module)

import services.llm_service as llm_service


class DummyNemoLLM:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_chat(self, model, chat_context):
        return {"choices": [{"message": {"content": f"{model}:{chat_context[0]['content']}"}}]}


class DummyBadNemoLLM:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_chat(self, model, chat_context):
        return {"unexpected": True}


def test_generate_success(monkeypatch):
    monkeypatch.setattr(llm_service, "NemoLLM", DummyNemoLLM)
    service = llm_service.LLMService("k", "m")
    assert service.generate("hi") == "m:hi"


def test_generate_fallback(monkeypatch):
    monkeypatch.setattr(llm_service, "NemoLLM", DummyBadNemoLLM)
    service = llm_service.LLMService("k", "m")
    assert service.generate("hi") == str({"unexpected": True})
