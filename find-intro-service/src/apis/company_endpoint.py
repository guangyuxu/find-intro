import json

import pandas as pd
from flask import request
from flask_restx import Namespace, Resource

from src.model.company_icp import CompanyInfo
from src.services.company.company_criteria import CompanyCriteria
from src.services.company.company_extractor import CompanyExtractor
from src.services.company.company_search import CompanySearcher
from src.services.company.company_vector_retriever import CompanyVectorRetriever

company_ns = Namespace('common', path='/api/company', description='company test endpoints')


@company_ns.route('/search')
class CompanySearcherAPI(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_search: CompanySearcher = CompanySearcher()

    def post(self):
        company_description = request.json['company_description']
        limit: int = request.json['limit']
        df: DataFrame = self.company_search.search(company_description, limit=limit)
        return json.loads(df.to_json())


@company_ns.route('/extract')
class TestCompanyExtractor(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_extractor = CompanyExtractor()

    def post(self):
        company_description = request.json['company_description']

        company_info: CompanyInfo = self.company_extractor.extract(company_description)
        return json.loads(company_info.json())


@company_ns.route('/criteria')
class TestCompanyCriteria(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_criteria = CompanyCriteria()

    def post(self):
        payload = request.json
        company_info: CompanyInfo = CompanyInfo(**payload)
        df: DataFrame = self.company_criteria.query(company_info)
        return json.loads(df.to_json())


@company_ns.route('/vector-retrieve')
class TestCompanyVectorRetriever(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_vector_retriever: CompanyVectorRetriever = CompanyVectorRetriever()

    def post(self):
        payload = request.json
        company_description = payload['company_description']
        company: CompanyInfo = CompanyInfo(**(request.json['company']))
        offset: int = int(request.json['offset'])
        limit: int = int(request.json['limit'])
        result_df = self.company_vector_retriever.retrieve(query=company_description, company=company, offset=offset, limit=limit)
        return json.loads(result_df.to_json())
