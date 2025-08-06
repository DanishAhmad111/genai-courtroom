import fitz  # PyMuPDF
import faiss
import os
import pickle
import numpy as np

from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# Load BGE model from Hugging Face using LangChain (CPU)
embedding_model = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# Extract full text from a PDF file
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Chunk long text into smaller segments (word-based)
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# -- Helpers for path handling --
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
EMB_DIR = os.path.join(BASE_DIR, "rag", "embeddings")
INDEX_PATH = os.path.join(EMB_DIR, "index.faiss")

# Create FAISS index from text chunks

def build_faiss_index(chunks, index_path: str = INDEX_PATH):
    """Build a FAISS vector index from text chunks and persist it to disk."""
    # Ensure embeddings directory exists
    os.makedirs(os.path.dirname(index_path), exist_ok=True)

    embeddings = embedding_model.embed_documents(chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, index_path)
    with open(index_path.replace(".faiss", ".pkl"), "wb") as f:
        pickle.dump(chunks, f)

# Search top-k most relevant chunks given a query
def search_top_chunks(query: str, index_path: str = INDEX_PATH, k: int = 3):
    """Return top-k relevant text chunks for a query from the FAISS index."""
    if not os.path.exists(index_path):
        raise FileNotFoundError("FAISS index not found. Build it first by uploading a PDF.")

    index = faiss.read_index(index_path)
    with open(index_path.replace(".faiss", ".pkl"), "rb") as f:
        chunks = pickle.load(f)
    query_embedding = embedding_model.embed_query(query)
    D, I = index.search(np.array([query_embedding]).astype("float32"), k)
    return [chunks[i] for i in I[0]]
