from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from src.env.env import *


class VectorHelper(object):
    def __init__(self):
        self._client = QdrantClient(host=VECTOR_QDRANT_HOST, port=VECTOR_QDRANT_PORT)
        self._model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
        self._dimension = int(SENTENCE_TRANSFORMER_DIMENSION)

    def get_qdrant_client(self) -> QdrantClient:
        return self._client

    def get_transformer_model(self) -> SentenceTransformer:
        return self._model

    def get_transformer_dimension(self) -> int:
        return self._dimension


vector_connection: VectorHelper = VectorHelper()
