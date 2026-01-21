import os
import faiss
import pickle
import numpy as np

try:
    from embedding import embed_query
except ImportError:
    # Handle direct execution
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from embedding.embedding import embed_query

# Define paths relative to this file to be robust
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels: src/embedding -> src -> root
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

INDEX_PATH = os.path.join(OUTPUT_DIR, "index.faiss")
METADATA_PATH = os.path.join(OUTPUT_DIR, "metadata.pkl")

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        self.load_index()

    def load_index(self):
        """Load FAISS index and metadata from disk on startup."""
        if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
            print("⚠️ Vector store not found. Please run the pipeline first.")
            return

        print("🔄 Loading vector store...")
        try:
            self.index = faiss.read_index(INDEX_PATH)
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)
            print(f"✅ Loaded {self.index.ntotal} vectors from index.")
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")

    def search(self, query: str, k: int = 3):
        """Search the index for the query text."""
        if not self.index:
            return []

        # 1. Embed the query using the retrieval_query task type
        query_vector = embed_query(query)
        
        # 2. Reshape for FAISS (1, dimension)
        query_vector = np.array([query_vector]).astype("float32")

        # 3. Search index
        distances, indices = self.index.search(query_vector, k)

        # 4. Map results to metadata
        results = []
        for i in range(k):
            idx = indices[0][i]
            if idx == -1: continue # No enough results
            
            result = {
                "chunk_id": self.metadata[idx]["chunk_id"],
                "text": self.metadata[idx]["text"],
                "score": float(distances[0][i])
            }
            results.append(result)
            
        return results

# Singleton instance for easy import
store = VectorStore()

if __name__ == "__main__":
    # Test search
    results = store.search("microprocessor architecture")
    for r in results:
        print(f"\n[Score: {r['score']:.4f}] Chunk {r['chunk_id']}")
        print(r['text'][:150] + "...")
