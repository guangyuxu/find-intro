import json
import logging

from pandas import DataFrame, read_sql_query

from src.connections.db_engine_helper import mysql_engine_helper
from src.model.company_icp import CompanyInfo, SampleJob
from sqlalchemy import Engine

logger = logging.getLogger(__name__)


class CompanyData(object):
    def __init__(self):
        self.engine_helper: MySQLEngineHelper = mysql_engine_helper

    def get_all_data(self) -> DataFrame:
        sql = f'select * from companies where CHAR_LENGTH(description) > 10'

        engine = self.engine_helper.get_mysql_engine()
        df: DataFrame = read_sql_query(sql, engine)
        df['industry'] = df['industry'].apply(json.loads)
        return df
