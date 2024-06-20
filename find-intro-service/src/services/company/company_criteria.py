import json
import logging

from pandas import DataFrame, read_sql_query

from src.connections.db_engine_helper import mysql_engine_helper
from src.model.company_icp import CompanyInfo, SampleJob
from sqlalchemy import Engine

logger = logging.getLogger(__name__)


def match_any(item_list: list[str], predefined_list: list[str]) -> bool:
    return any(item in predefined_list for item in item_list)


class CompanyCriteria(object):
    def __init__(self):
        self.engine_helper: MySQLEngineHelper = mysql_engine_helper

    def query(self, company: CompanyInfo) -> DataFrame:
        conditions = []
        params = {}
        if company.countries:
            conditions.append(f"location_country in %(countries)s")
            params["countries"] = company.countries
        if company.minimum_headcount:
            conditions.append(f"(number_of_employees >= %(minimum_headcount)s or number_of_employees=0)")
            params["minimum_headcount"] = company.minimum_headcount
        if company.funding_stages:
            conditions.append(f"investment_stage in %(funding_stages)s")
            params["funding_stages"] = company.funding_stages

        sql = f'select * from companies where {" and ".join(conditions)}'
        logger.info(sql, params)
        engine = self.engine_helper.get_mysql_engine()
        df: DataFrame = read_sql_query(sql, engine, params=params)
        df['industry'] = df['industry'].apply(json.loads)

        if company.industries:
            df = df[df['industry'].apply(lambda x: match_any(x, company.industries))]
        return df
