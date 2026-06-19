import os
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = os.path.join(os.getcwd(), "chromadb_data")

# Global variables
chroma_client = None
collection = None
embedding_function = None


def get_collection():
    global chroma_client, collection, embedding_function

    if collection is None:
        print("Loading ChromaDB and Embedding Model...")

        chroma_client = chromadb.PersistentClient(path=DB_PATH)

        embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

        collection = chroma_client.get_or_create_collection(
            name="edu_knowledge_base",
            embedding_function=embedding_function
        )

        print("ChromaDB Ready!")

    return collection


def ingest_knowledge(text_content: str, source_name: str):

    collection = get_collection()

    print(f"Ingesting data from: {source_name}")

    chunks = text_content.split("\n\n")
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 10]

    ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name} for _ in range(len(chunks))]

    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )

    return f"Successfully saved {len(chunks)} chunks."


def search_knowledge(query: str, n_results: int = 2):

    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results["documents"][0]