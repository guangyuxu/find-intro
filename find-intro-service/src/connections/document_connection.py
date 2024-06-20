from elasticsearch import Elasticsearch
from pinecone import Pinecone
from pinecone.data.index import Index
from sqlalchemy import create_engine, Engine

from src.env.env import *

_mysql_connection_string = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'


def connect_elasticsearch() -> Elasticsearch:
    return Elasticsearch(hosts=[f'https://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'],
                         basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD), verify_certs=False)


_mysql_engine: Engine = create_engine(_mysql_connection_string)
_es: Elasticsearch = connect_elasticsearch()
_pinecone_index: Index = Pinecone(api_key=PINECONE_API_KEY).Index(PINECONE_INDEX_NAME)


def get_mysql_engine():
    global _mysql_engine
    if _mysql_engine is None:
        _mysql_engine = create_engine(MYSQL_CONNECTION_STRING)
    return _mysql_engine


def get_elasticsearch_connection() -> Elasticsearch:
    global _es
    if _es is not None and _es.ping():
        return _es
    else:
        _es = connect_elasticsearch()
        return _es


def get_pinecone_connection() -> Index:
    global _pinecone_index
    if _pinecone_index is None:
        _pinecone_index = Pinecone(api_key=PINECONE_API_KEY).Index(PINECONE_INDEX_NAME)

    return _pinecone_index
