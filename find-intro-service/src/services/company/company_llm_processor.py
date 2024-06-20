import logging
from datetime import datetime
from io import StringIO

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pandas import DataFrame

from src.env.env import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL_NAME, OPENAI_TEMPERATURE
from src.model.company_icp import CompanyInfo

logger = logging.getLogger(__name__)

template = f'''
You are a professional recruiter with extensive experience in searching for companies on LinkedIn.
I will provide you a company description for the ideal company an individual should be working at, with a set of company profiles


Your Task:
======
Reorder these profiles based on their match to the original company description. Please exclude Company Headcount, Company Industry, and Funding Stage from your matching criteria.
For each company, provide a match score. Use GPT-4's natural language understanding capabilities to perform fine-grained semantic comparisons. Apply weights to different attribute scores to compute the final match score(0.01~1.00).


Input
======
**Original Company Description:**
{{company_description}}

**Company Profiles to Evaluate:**
company_id, company_name, location state, location city, description
{{company_list_csv}}



The output should be a JSON list of dictionaries, where the keys are company_id, company_name, and match_score. 
======
{{format_instructions}}
'''


class CompanyLLMProcessor(object):
    def __init__(self):
        self.llm: ChatOpenAI = ChatOpenAI(model=OPENAI_MODEL_NAME, temperature=OPENAI_TEMPERATURE,
                                          openai_api_base=OPENAI_API_BASE, openai_api_key=OPENAI_API_KEY)

    @staticmethod
    def get_additional_attributes(company: CompanyInfo) -> str:
        attributes = []
        if company.department_specific_headcount:
            attributes.append(f'Department-specific headcount: {company.department_specific_headcount}')
        if company.annual_spend:
            attributes.append(f'Annual Spend: ${company.annual_spend}')
        if company.software_tools:
            attributes.append(f"Uses X software: {company.software_tools}")
        return "\n".join(attributes)

    @staticmethod
    def get_company_list_csv(df: DataFrame) -> str:
        csv_buffer = StringIO()
        df[["id", "name", "location_state", "location_city", "description"]].to_csv(csv_buffer, index=False)
        csv_text = csv_buffer.getvalue()
        return csv_text

    def process(self, company_description, df: DataFrame) -> DataFrame:
        parser: JsonOutputParser = JsonOutputParser()
        prompt = PromptTemplate(
            template=template,
            input_variables=["company_description", "additional_attributes", "company_list_csv"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser
        start = datetime.now().timestamp()
        result = chain.invoke({
            "company_description": company_description,
            "company_list_csv": self.get_company_list_csv(df)
        })
        end = datetime.now().timestamp()
        logger.info(f'Time cost of extracting company: {end - start}')
        return DataFrame(result)
