import logging
import logging_config

from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, fields, Namespace, Resource

from src.model.company_icp import CompanyRawICP
from src.services.main_service import MainService
from src.apis.common_endpoint import common_ns
from src.apis.company_endpoint import company_ns

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_namespace(common_ns)
api.add_namespace(company_ns)

logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
