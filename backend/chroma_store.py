"""
Shared ChromaDB collection - lazy initialized so it loads after .env is ready.
"""
import chromadb

_client = None
_collection = None


def get_collection():
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path="./chroma_data")
    if _collection is None:
        try:
            _collection = _client.get_collection(name="documents")
        except Exception:
            _collection = _client.create_collection(name="documents")
    return _collection
