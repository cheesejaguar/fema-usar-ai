import os
import chromadb
from chromadb.config import Settings

class VectorStoreService:
    def __init__(self, persist_directory=None):
        self.persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection("documents")

    def add(self, embeddings, metadatas):
        ids = [str(i) for i in range(len(embeddings))]
        self.collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)

    def query(self, query_embedding, n_results=5):
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
