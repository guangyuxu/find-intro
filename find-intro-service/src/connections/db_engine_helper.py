from sqlalchemy import create_engine, Engine

from src.env.env import *

_mysql_connection_string = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
_mysql_engine: Engine = create_engine(_mysql_connection_string)


class MySQLEngineHelper(object):
    def __init__(self):
        self.engine: Engine = create_engine(_mysql_connection_string)

    def get_mysql_engine(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(MYSQL_CONNECTION_STRING)
        return self.engine


mysql_engine_helper: MySQLEngineHelper = MySQLEngineHelper()
