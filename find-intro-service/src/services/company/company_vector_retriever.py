import logging

from pandas import DataFrame
from qdrant_client.http.models import MatchAny
from qdrant_client.models import Filter, FieldCondition, Range

from src.connections.vector_connection import vector_connection, VectorHelper
from src.env.env import VECTOR_QDRANT_COLLECTION_COMPANY_NAME
from src.model.company_icp import CompanyInfo

logger = logging.getLogger(__name__)


class CompanyVectorRetriever(object):
    def __init__(self):
        self.vector_connection: VectorHelper = vector_connection
        self.client: QdrantClient = vector_connection.get_qdrant_client()
        self.model: SentenceTransformer = vector_connection.get_transformer_model()

    def retrieve(self, query: str, company: CompanyInfo, offset: int = 0, limit: int = 10) -> DataFrame:
        query_embedding = self.model.encode(query).tolist()

        query_filter: Filter = self.build_filter(company=company)

        search_result = self.client.search(
            collection_name=VECTOR_QDRANT_COLLECTION_COMPANY_NAME,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=limit,
            offset=offset,
            with_payload=True
        )

        print(f"Top {len(search_result)} documents based on similarity:")
        results = []
        for hit in search_result:
            logger.info(f"Document ID: {hit.id}, Score: {hit.score:.4f}, Text: {hit.payload}")
            industries = hit.payload['industry']
            if not company.industries or bool(set(company.industries) & set(industries)):
                payload = hit.payload
                payload.update({
                    "id": hit.id,
                    "score": hit.score
                })
                results.append(payload)
        return DataFrame(results)

    @staticmethod
    def build_filter(company: CompanyInfo) -> Filter:
        filter_conditions = []

        if company.countries:
            filter_conditions.append(
                FieldCondition(
                    key="location_country",
                    match=MatchAny(any=company.countries)
                )
            )
        if company.minimum_headcount:
            filter_conditions.append(
                Filter(
                    should=[
                        FieldCondition(
                            key="number_of_employees",
                            range=Range(
                                gte=company.minimum_headcount
                            )
                        ),
                        FieldCondition(
                            key="number_of_employees",
                            match=MatchAny(any=[0])
                        )
                    ]
                )
            )

        if company.funding_stages:
            filter_conditions.append(
                FieldCondition(
                    key="investment_stage",
                    match=MatchAny(any=company.funding_stages)
                )
            )

        if company.industries:
            industry_conditions = []
            for value in company.industries:
                industry_conditions.append(FieldCondition(
                    key="industry",
                    match=MatchAny(any=[value])
                ))

            filter_conditions.append(
                Filter(should=industry_conditions)
            )

        return Filter(must=filter_conditions)
