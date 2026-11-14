# app/vectorstore.py
"""
Vectorstore module for InternGuide using ChromaDB.
Provides persistent Chroma collection creation, indexing of chunked documents,
and similarity query functions.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
from chromadb.config import Settings
from app.chunking import chunk_all_documents

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"
DEFAULT_COLLECTION_NAME = "internguide"


def get_client(persist_dir: Optional[Path] = None) -> chromadb.PersistentClient:
    """Initialize and return a persistent Chroma client."""
    path = persist_dir or CHROMA_DIR
    path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(path),
        settings=Settings(anonymized_telemetry=False)
    )


def get_or_create_collection(
    client: Optional[chromadb.PersistentClient] = None,
    collection_name: str = DEFAULT_COLLECTION_NAME
) -> chromadb.Collection:
    """Retrieve or create the named persistent collection."""
    if client is None:
        client = get_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "InternGuide AICTE, UGC, and PMIS policy chunks"}
    )


def index_chunks(
    chunks: Optional[List[Dict[str, Any]]] = None,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    batch_size: int = 100
) -> int:
    """
    Index all chunked documents into the persistent Chroma collection.
    Skips existing IDs or updates them in batches.
    """
    if chunks is None:
        chunks = chunk_all_documents()

    if not chunks:
        print("No chunks provided or found to index.")
        return 0

    client = get_client()
    collection = get_or_create_collection(client, collection_name)

    total = len(chunks)
    print(f"Indexing {total} chunks into persistent collection '{collection_name}' at {CHROMA_DIR}...")

    # Insert in batches
    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        ids = [c["id"] for c in batch]
        documents = [c["text"] for c in batch]
        metadatas = [c["metadata"] for c in batch]

        # Use upsert so indexing is idempotent and safe to re-run
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"  Indexed batch {i // batch_size + 1} ({len(batch)} chunks)")

    count = collection.count()
    print(f"Done! Collection '{collection_name}' now contains {count} total indexed chunks.")
    return count


def query_vectorstore(
    query: str,
    top_k: int = 5,
    collection_name: str = DEFAULT_COLLECTION_NAME
) -> List[Dict[str, Any]]:
    """
    Perform semantic search over the persistent Chroma collection.
    Returns ranked list of hits with text, metadata (source, page, title), and distance.
    """
    client = get_client()
    collection = get_or_create_collection(client, collection_name)

    if collection.count() == 0:
        print("Collection is empty. Automatically indexing all documents...")
        index_chunks(collection_name=collection_name)

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    hits = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
        ids = results["ids"][0] if "ids" in results else [""] * len(docs)
        distances = results["distances"][0] if "distances" in results else [0.0] * len(docs)

        for doc_id, doc_text, meta, dist in zip(ids, docs, metas, distances):
            hits.append({
                "id": doc_id,
                "text": doc_text,
                "source": meta.get("source", "unknown"),
                "page": meta.get("page", 0),
                "title": meta.get("title", "InternGuide"),
                "distance": round(float(dist), 4),
                "similarity_score": round(1.0 / (1.0 + float(dist)), 4)
            })

    return hits


if __name__ == "__main__":
    count = index_chunks()
    print(f"\nTesting vectorstore query: 'How many hours is one internship credit?'")
    results = query_vectorstore("How many hours is one internship credit?", top_k=2)
    for r in results:
        print(f"[{r['source']} | Page {r['page']} | Score {r['similarity_score']}]")
        print(f"{r['text'][:140]}...\n")
