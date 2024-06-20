import os

from transformers import AutoModel, AutoTokenizer

OPENAI_API_BASE = None if os.getenv("OPENAI_API_BASE", None) is None or os.getenv("OPENAI_API_BASE", None) == '' else os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", 'gpt-4o')
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))


MYSQL_HOST: str = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT: str = "3306"
MYSQL_USERNAME: str = os.getenv('MYSQL_USERNAME', 'findintro')
MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD', 'findintro')
MYSQL_DATABASE: str = os.getenv('MYSQL_DATABASE', 'findintro')

VECTOR_QDRANT_HOST: str = os.getenv("VECTOR_QDRANT_HOST", 'localhost')
VECTOR_QDRANT_PORT: int = int(os.getenv("VECTOR_QDRANT_PORT", "6333"))
VECTOR_QDRANT_COLLECTION_COMPANY_NAME: str = "companies"

# (dimension=384) paraphrase-MiniLM-L12-v2: Good for slightly better performance without a significant increase in resources.
# paraphrase-mpnet-base-v2: Better performance for longer texts but more resource-intensive.
# all-mpnet-base-v2: Excellent all-around model with high performance.
SENTENCE_TRANSFORMER_MODEL: str = os.getenv('SENTENCE_TRANSFORMER_MODEL', 'paraphrase-MiniLM-L12-v2')
SENTENCE_TRANSFORMER_DIMENSION: str = os.getenv('SENTENCE_TRANSFORMER_DIMENSION', "384")

# CROSS_ENCODER_MODEL: str = os.getenv("CROSS_ENCODER_MODEL", 'cross-encoder/ms-marco-MiniLM-L-6-v2')

LOGGING_LEVEL: str = os.getenv('LOGGING_LEVEL', 'INFO')
