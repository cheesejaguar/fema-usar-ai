from services.vector_store import VectorStoreService


def test_vector_store_add_and_query(tmp_path):
    service = VectorStoreService(persist_directory=str(tmp_path))
    assert service.persist_directory == str(tmp_path)

    service.add([[1.0, 0.0], [0.0, 1.0]], [{"source": "a"}, {"source": "b"}])

    result = service.query([0.9, 0.1], n_results=2)
    assert [m["source"] for m in result["metadatas"][0]] == ["a", "b"]
    assert result["distances"][0][0] < result["distances"][0][1]

    result = service.query([0.1, 0.9], n_results=1)
    assert result["metadatas"] == [[{"source": "b"}]]


def test_vector_store_persists_to_directory(tmp_path):
    VectorStoreService(persist_directory=str(tmp_path)).add([[1.0, 0.0]], [{"source": "a"}])

    reopened = VectorStoreService(persist_directory=str(tmp_path))
    assert reopened.collection.count() == 1
    assert reopened.query([1.0, 0.0], n_results=1)["metadatas"] == [[{"source": "a"}]]


def test_vector_store_add_twice_keeps_both_batches(tmp_path):
    service = VectorStoreService(persist_directory=str(tmp_path))

    service.add([[1.0, 0.0]], [{"source": "first"}])
    service.add([[0.0, 1.0]], [{"source": "second"}])

    assert service.collection.count() == 2
    assert service.query([0.0, 1.0], n_results=1)["metadatas"] == [[{"source": "second"}]]


def test_vector_store_uses_env_directory_by_default(tmp_path, monkeypatch):
    monkeypatch.setenv("CHROMA_PERSIST_DIRECTORY", str(tmp_path / "env_db"))

    service = VectorStoreService()

    assert service.persist_directory == str(tmp_path / "env_db")
    assert (tmp_path / "env_db").is_dir()
