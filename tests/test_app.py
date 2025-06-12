import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import types

# Provide dummy external modules before importing app
class DummyLimiter:
    def __init__(self, app, key_func=None, default_limits=None):
        self.app = app

class DummyLLMService:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key
        self.model = model
    def generate(self, msg):
        return f"reply:{msg}"

class DummyVectorStoreService:
    def __init__(self, persist_directory=None):
        self.persist_directory = persist_directory

# Stubs for heavy dependencies
sys.modules.setdefault("nemollm", types.ModuleType("nemollm"))
sys.modules["nemollm"].NemoLLM = object
sys.modules.setdefault("chromadb", types.ModuleType("chromadb"))
sys.modules["chromadb"].PersistentClient = object
sys.modules.setdefault("chromadb.config", types.ModuleType("chromadb.config"))
sys.modules["chromadb.config"].Settings = object

import app as app_module


def make_app(monkeypatch):
    monkeypatch.setattr(app_module, "Limiter", DummyLimiter)
    monkeypatch.setattr("services.llm_service.LLMService", DummyLLMService)
    monkeypatch.setattr("services.vector_store.VectorStoreService", DummyVectorStoreService)
    monkeypatch.setattr(app_module, "LLMService", DummyLLMService)
    monkeypatch.setattr(app_module, "VectorStoreService", DummyVectorStoreService)
    return app_module.create_app()


def test_create_app(monkeypatch):
    flask_app = make_app(monkeypatch)
    assert isinstance(flask_app.llm_service, DummyLLMService)
    assert isinstance(flask_app.vector_store, DummyVectorStoreService)
    assert isinstance(flask_app.limiter, DummyLimiter)


def test_chat_route(monkeypatch):
    flask_app = make_app(monkeypatch)
    flask_app.config["API_KEY"] = "token"
    client = flask_app.test_client()

    resp = client.post("/api/chat", json={"message": "hi"}, headers={"X-API-Key": "token"})
    assert resp.status_code == 200
    assert resp.get_json() == {"response": "reply:hi"}

    resp = client.post("/api/chat", json={}, headers={"X-API-Key": "token"})
    assert resp.status_code == 400

    resp = client.post("/api/chat", json={"message": "hi"})
    assert resp.status_code == 401
