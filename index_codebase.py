import os
import chromadb
# from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Persistent ChromaDB setup
client = chromadb.PersistentClient(path="/home/rahul/projects/rails_ollama_rag/.chroma")
collection = client.get_or_create_collection("rails_codebase")

# print("[DEBUG] Client type:", type(client))

# Load model (fallback to CPU if GPU fails)
try:
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
except Exception as e:
    print(f"[⚠️] CUDA failed, using CPU: {e}")
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

def index_codebase(code_path="./app"):
    count = 0
    for root, _, files in os.walk(code_path):
        for file in files:
            if file.endswith(".rb"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read().strip()
                    if not code:
                        continue

                    embedding = model.encode(code)
                    collection.add(
                        documents=[code],
                        embeddings=[embedding.tolist()],
                        ids=[file_path]
                    )
                    count += 1
    # client.persist()  # ✅ Persist to disk
    print(f"[✅] Total indexed: {count}")

if __name__ == "__main__":
    index_codebase()  # change this
