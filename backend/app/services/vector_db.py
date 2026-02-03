import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorService, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """
        Initialize Qdrant client and Embedding model.
        """
        logger.info("Initializing Vector Service...")
        
        # 1. Initialize Qdrant (Local)
        # Using a local directory for persistence
        self.client = QdrantClient(path="storage/qdrant_db")
        self.collection_name = "vidsage_knowledge"
        
        # 2. Initialize Model (MiniLM)
        # Verify if GPU is available (optional, defaults to CPU)
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise e

        # 3. Create Collection if not exists
        try:
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' exists.")
        except Exception:
            logger.info(f"Creating collection '{self.collection_name}'...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def embed_text(self, text: str) -> list[float]:
        """
        Convert text to vector embedding.
        """
        return self.model.encode(text).tolist()

    def upsert_chunks(self, video_id: str, chunks: list[dict]):
        """
        Index chunks into Qdrant.
        chunks: List of dicts with 'text', 'chunk_id', 'type'
        """
        points = []
        for i, chunk in enumerate(chunks):
            vector = self.embed_text(chunk['text'])
            
            # Create a deterministic ID or random UUID
            # Ideally combine video_id + chunk_index
            
            points.append(PointStruct(
                id=i,  # Ideally unique UUID, but simple index for now if scoped? 
                       # Qdrant IDs must be Unique/UUID. Let's rely on auto-generation or composite.
                       # Actually, let's use a hash or UUID for robust ID.
                vector=vector,
                payload={
                    "video_id": video_id,
                    "text": chunk['text'],
                    "type": chunk.get('type', 'general'),
                    "chunk_id": chunk.get('chunk_id', i)
                }
            ))
        
        # Using UUID generation for points to avoid collision
        import uuid
        unique_points = []
        for p in points:
             # Re-create point with UUID
             unique_points.append(PointStruct(
                 id=str(uuid.uuid4()),
                 vector=p.vector,
                 payload=p.payload
             ))

        self.client.upsert(
            collection_name=self.collection_name,
            points=unique_points
        )
        logger.info(f"Indexed {len(unique_points)} chunks for video {video_id}")

    def search(self, query: str, limit: int = 5, score_threshold: float = 0.0) -> list[dict]:
        """
        Search for relevant chunks.
        """
        query_vector = self.embed_text(query)
        
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        
        results = []
        for hit in hits:
            results.append({
                "score": hit.score,
                "text": hit.payload.get("text"),
                "type": hit.payload.get("type"),
                "video_id": hit.payload.get("video_id")
            })
            
        return results

# Singleton accessor
def get_vector_service():
    return VectorService()
