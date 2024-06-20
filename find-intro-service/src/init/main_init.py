import numpy as np

from src.env.env import VECTOR_QDRANT_COLLECTION_COMPANY_NAME
from src.init.company_data import CompanyData
from src.init.company_vector_init import CompanyVectorInitializer


class MainInitializer(object):

    def __init__(self):
        self.company_data: CompanyData = CompanyData()
        self.company_vector_initializer: CompanyVectorInitializer = CompanyVectorInitializer()
        self.page_size = 20

    def load_all(self) -> int:
        return self.load_company_vector()

    def load_company_vector(self) -> int:
        df: DataFrame = self.company_data.get_all_data()
        df = df.rename(columns={"organization_id": "id"})
        df = df.sort_values(ascending=False, by=["id"])

        df_split = np.array_split(df, len(df) // self.page_size + (1 if len(df) % self.page_size != 0 else 0))

        for df_slot in df_split:
            self.company_vector_initializer.load(df_slot)
        return len(df)
