from flask import request
from flask_restx import fields, Namespace, Resource

from src.init.main_init import MainInitializer
from src.model.company_icp import CompanyRawICP
from src.services.main_service import MainService

common_ns = Namespace('common', path='/api/v1', description='common endpoints')
CompanyRawICPApiModel = common_ns.model('CompanyICPApiModel', {
    'company_name': fields.String(required=True, description='Company Name'),
    'job_titles': fields.String(required=False, description='Job Titles'),
    'company_description': fields.String(required=False, description='Company Description'),
})


@common_ns.route('/search')
class SearchRefine(Resource):
    @common_ns.expect(CompanyRawICPApiModel)
    def post(self):
        payload = request.json
        company_raw_icp = CompanyRawICP(**payload)
        MainService().find_intro(company_raw_icp=company_raw_icp)

        return 1


@common_ns.route('/load-all')
class MainInitWrapper(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_initializer: MainInitializer = MainInitializer()
    def put(self) -> int:
        return self.main_initializer.load_all()