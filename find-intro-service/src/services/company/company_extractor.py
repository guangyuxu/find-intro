from datetime import datetime

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pandas import read_sql_query
from sqlalchemy import Engine

from src.connections.db_engine_helper import mysql_engine_helper
from src.env.env import OPENAI_API_BASE, OPENAI_API_KEY, OPENAI_MODEL_NAME, OPENAI_TEMPERATURE
from src.model.company_icp import CompanyInfo

engine: Engine = mysql_engine_helper.get_mysql_engine()

# existing_job_functions = read_sql_query("select distinct job_function from connection_data", engine)["job_function"].tolist()
# existing_job_seniority = read_sql_query("select distinct job_seniority from connection_data", engine)["job_seniority"].tolist()
countries = read_sql_query("select name from countries", engine)["name"].tolist()
industries = read_sql_query("select name from industries", engine)["name"].tolist()
funding_stages = read_sql_query("select name from investment_stages", engine)["name"].tolist()

company_template = f'''
You are a professional recruiter with extensive experience in searching for companies on LinkedIn.

I will provide you with a <Company Description> in free text format, along with <Country List>, <Industry List>, and <Funding Stage List> data sets.

Your task is to extract the information from the <Company Description>, and return a json without and additional and markdown information. Return json keys are: countries, minimum_headcount, department_specific_headcount, industries, funding_stages, annual_spend, software_tools. The detail of keys is described at the end of the prompt


Company Description
======
{{company_description}}



**Country List: 
======
{countries}

Industry List: 
======
{industries}

Funding Stage List:
====== 
{funding_stages}



{{format_instructions}}
'''


class CompanyExtractor(object):
    def __init__(self):
        self.llm: ChatOpenAI = ChatOpenAI(model=OPENAI_MODEL_NAME, temperature=OPENAI_TEMPERATURE,
                                          openai_api_base=OPENAI_API_BASE, openai_api_key=OPENAI_API_KEY)

    def extract(self, company_description: str) -> CompanyInfo:
        parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=CompanyInfo)
        prompt = PromptTemplate(
            template=company_template,
            input_variables=["company_description"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser
        start = datetime.now().timestamp()
        company_info: CompanyInfo = chain.invoke({"company_description": company_description})
        end = datetime.now().timestamp()
        print(f'Time cost of extracting company: {end - start}')
        return company_info
