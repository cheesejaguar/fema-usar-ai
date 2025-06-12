import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import types

# Provide dummy chromadb module before import
class DummyCollection:
    def __init__(self):
        self.add_calls = []
        self.queries = []
    def add(self, embeddings, metadatas, ids):
        self.add_calls.append((embeddings, metadatas, ids))
    def query(self, query_embeddings, n_results):
        self.queries.append((query_embeddings, n_results))
        return {"results": n_results}

class DummyClient:
    def __init__(self, path):
        self.path = path
        self.collection = DummyCollection()
    def get_or_create_collection(self, name):
        return self.collection

dummy_chromadb = types.SimpleNamespace(PersistentClient=DummyClient)
sys.modules.setdefault("chromadb", dummy_chromadb)
sys.modules.setdefault("chromadb.config", types.ModuleType("chromadb.config"))
sys.modules["chromadb.config"].Settings = object

import services.vector_store as vector_store


def test_vector_store_add_and_query(monkeypatch, tmp_path):
    # Replace chromadb with dummy implementation
    monkeypatch.setattr(vector_store, "chromadb", dummy_chromadb)

    service = vector_store.VectorStoreService(persist_directory=str(tmp_path))
    assert service.persist_directory == str(tmp_path)

    embeddings = [[0.1, 0.2]]
    metas = [{"id": 1}]
    service.add(embeddings, metas)
    assert service.collection.add_calls[0][0] == embeddings

    result = service.query([0.3, 0.4], n_results=3)
    assert result == {"results": 3}
    assert service.collection.queries[0] == ([[0.3, 0.4]], 3)
