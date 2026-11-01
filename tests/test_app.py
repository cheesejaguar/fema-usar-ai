import pytest
from flask_limiter import Limiter

from app import create_app
from config import TestingConfig
from services.llm_service import LLMService
from services.vector_store import VectorStoreService


@pytest.fixture
def flask_app(fake_nemo, tmp_path):
    class Cfg(TestingConfig):
        API_KEY = "token"
        NEMO_API_KEY = "nemo-key"
        DEFAULT_MODEL = "test-model"
        CHROMA_PERSIST_DIRECTORY = str(tmp_path / "chroma")

    return create_app(Cfg)


def test_create_app(flask_app, fake_nemo, tmp_path):
    assert isinstance(flask_app.llm_service, LLMService)
    assert flask_app.llm_service.model == "test-model"
    assert fake_nemo.instances[0].api_key == "nemo-key"

    assert isinstance(flask_app.vector_store, VectorStoreService)
    assert flask_app.vector_store.persist_directory == str(tmp_path / "chroma")

    assert isinstance(flask_app.limiter, Limiter)


def test_chat_route(flask_app, fake_nemo):
    client = flask_app.test_client()

    resp = client.post("/api/chat", json={"message": "hi"}, headers={"X-API-Key": "token"})
    assert resp.status_code == 200
    assert resp.get_json() == {"response": "reply:hi"}
    assert fake_nemo.instances[0].calls == [
        {"model": "test-model", "chat_context": [{"role": "user", "content": "hi"}]}
    ]

    resp = client.post("/api/chat", json={}, headers={"X-API-Key": "token"})
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "message required"}

    resp = client.post("/api/chat", json={"message": "hi"})
    assert resp.status_code == 401

    resp = client.post("/api/chat", json={"message": "hi"}, headers={"X-API-Key": "wrong"})
    assert resp.status_code == 401

    # Rejected requests must never reach the LLM.
    assert len(fake_nemo.instances[0].calls) == 1


def test_ics205_route(flask_app, fake_nemo):
    client = flask_app.test_client()

    incident = "Test"
    prompt = (
        f"Prepare an ICS 205 Incident Radio Communications Plan for this incident: {incident}. "
        "Return the plan as a Markdown table."
    )
    resp = client.post("/api/ics205", json={"incident": incident}, headers={"X-API-Key": "token"})
    assert resp.status_code == 200
    assert resp.get_json() == {"ics205": f"reply:{prompt}"}
    assert fake_nemo.instances[0].calls == [
        {"model": "test-model", "chat_context": [{"role": "user", "content": prompt}]}
    ]

    resp = client.post("/api/ics205", json={}, headers={"X-API-Key": "token"})
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "incident required"}

    resp = client.post("/api/ics205", json={"incident": incident})
    assert resp.status_code == 401
    assert len(fake_nemo.instances[0].calls) == 1
