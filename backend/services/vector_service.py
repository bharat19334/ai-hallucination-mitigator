import os
import chromadb
from chromadb.utils import embedding_functions


DB_PATH = os.path.join(os.getcwd(), "chromadb_data")
chroma_client = chromadb.PersistentClient(path=DB_PATH)


sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = chroma_client.get_or_create_collection(
    name="edu_knowledge_base", 
    embedding_function=sentence_transformer_ef
)

def ingest_knowledge(text_content: str, source_name: str):
    
    print(f"Ingesting data from: {source_name}...")
    
    chunks = text_content.split("\n\n") 

    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 10]

    ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]

    metadatas = [{"source": source_name} for _ in range(len(chunks))]
    
 
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    return f"Successfully saved {len(chunks)} chunks to Database."

def search_knowledge(query: str, n_results: int = 2):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results['documents'][0]