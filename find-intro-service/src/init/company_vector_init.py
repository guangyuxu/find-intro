import logging

from pandas import DataFrame
from qdrant_client.models import PointStruct, Distance, VectorParams

from src.connections.vector_connection import vector_connection, VectorHelper
from src.env.env import VECTOR_QDRANT_COLLECTION_COMPANY_NAME

logger = logging.getLogger(__name__)


class CompanyVectorInitializer(object):
    def __init__(self):
        self.vector_connection: VectorHelper = vector_connection
        self.client: QdrantClient = vector_connection.get_qdrant_client()
        self.model: SentenceTransformer = vector_connection.get_transformer_model()
        self.dimension: int = vector_connection.get_transformer_dimension()

    def load(self, df: DataFrame) -> int:
        self.check_collection_exists()

        df["embedding"] = df["description"].apply(lambda x: self.model.encode(x).tolist())

        logger.info(df["id"].tolist())

        points = [
            PointStruct(id=int(row['id']), vector=row['embedding'], payload={
                "name": row["name"],
                "website": row["website"],
                "description": row["description"],
                "number_of_employees": row["number_of_employees"],
                "investment_stage": row["investment_stage"],
                "location_city": row["location_city"],
                "location_state": row["location_state"],
                "location_country": row["location_country"],
                "industry": row["industry"],
                "industry_lower": row["industry_lower"],
            })
            for index, row in df.iterrows()
        ]
        self.client.upsert(collection_name=VECTOR_QDRANT_COLLECTION_COMPANY_NAME, points=points, wait=True)
        return len(df)

    def check_collection_exists(self) -> bool:
        try:
            collections = self.client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            if VECTOR_QDRANT_COLLECTION_COMPANY_NAME in collection_names:
                print(f"Collection '{VECTOR_QDRANT_COLLECTION_COMPANY_NAME}' already exists.")
            else:
                raise Exception(f"Collection '{VECTOR_QDRANT_COLLECTION_COMPANY_NAME}' doesn't exist.")
        except Exception as e:
            print(f"Error: {e}")
            print("Creating the collection...")

            self.client.create_collection(
                collection_name=VECTOR_QDRANT_COLLECTION_COMPANY_NAME,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=Distance.COSINE
                )
            )
            print(f"Collection '{VECTOR_QDRANT_COLLECTION_COMPANY_NAME}' created with cosine similarity.")
