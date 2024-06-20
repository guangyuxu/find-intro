from src.model.company_icp import CompanyRawICP
from src.services.company.company_search import CompanySearcher


class MainService(object):
    def __init__(self):
        self.company_searcher: CompanySearcher = CompanySearcher()

    def find_intro(self, company_raw_icp: CompanyRawICP):
        self.company_searcher.search(company_raw_icp.company_description)
