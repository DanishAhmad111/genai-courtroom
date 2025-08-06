from rag.rag_utils import extract_text_from_pdf, chunk_text, build_faiss_index

# Step 1: Extract and chunk text
text = extract_text_from_pdf("rag/constitution.pdf")
chunks = chunk_text(text)

# Step 2: Build FAISS index
build_faiss_index(chunks, index_path="rag/embeddings/index.faiss")

print("✅ FAISS index for Indian Constitution built.")
