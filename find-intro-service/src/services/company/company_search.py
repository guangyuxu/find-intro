import logging

import numpy as np
from pandas import DataFrame, concat, merge
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.model.company_icp import CompanyInfo
from src.services.company.company_criteria import CompanyCriteria
from src.services.company.company_extractor import CompanyExtractor
from src.services.company.company_llm_processor import CompanyLLMProcessor
from src.services.company.company_vector_retriever import CompanyVectorRetriever

logger = logging.getLogger(__name__)


class CompanySearcher(object):
    def __init__(self):
        self.company_extractor: CompanyExtractor = CompanyExtractor()
        self.company_criteria: CompanyCriteria = CompanyCriteria()
        self.company_vector_retriever: CompanyVectorRetriever = CompanyVectorRetriever()
        self.company_llm_processor: CompanyLLMProcessor = CompanyLLMProcessor()
        self.page_size = 5

    def search(self, company_description: str, limit: int = 10) -> DataFrame:
        company: CompanyInfo = self.company_extractor.extract(company_description)

        pre_limit = int(limit * 1.5)

        df: DataFrame = self.company_vector_retriever.retrieve(query=company_description, company=company,
                                                               limit=pre_limit)
        df = df.rename(columns={"score": "vector_score"})

        df_split = np.array_split(df, len(df) // self.page_size + (1 if len(df) % self.page_size != 0 else 0))
        rescored_df_list = []
        with ThreadPoolExecutor(max_workers=len(df_split)) as executor:
            futures = [executor.submit(self.company_llm_processor.process, company_description, df_part) for
                       df_part in df_split]
            for future in as_completed(futures):
                rescored_df_list.append(future.result())

        rescored_df: DataFrame = concat(rescored_df_list)
        rescored_df = rescored_df.reset_index(drop=True)
        rescored_df = rescored_df.rename(columns={"company_id": "id"})

        merged_df = merge(df, rescored_df, how="inner", on="id")
        merged_df = merged_df.drop(columns="company_name")
        merged_df = merged_df.sort_values(by="match_score", ascending=False)

        return merged_df.head(limit)
