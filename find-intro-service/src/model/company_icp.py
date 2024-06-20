from typing import List, Optional

from pydantic import BaseModel

from langchain_core.pydantic_v1 import BaseModel as LangChainBaseModel, Field as LangChainField


class CompanyRawICP(BaseModel):
    company_name: str
    job_titles: str
    company_description: str

    class Config:
        arbitrary_types_allowed = True


class SampleJob(LangChainBaseModel):
    job_title: str = LangChainField(required=True, description="A grouped job title")
    job_function: list[str] = LangChainField(required=True, description="The specific role or set of responsibilities that an employee has within an organization. It typically describes what the employee does on a day-to-day basis")
    job_seniority: Optional[str] = LangChainField(required=False, description="The level or rank of an employee within the organizational hierarchy. It indicates the level of experience, responsibility, and authority the employee has.")


class SampleJobs(LangChainBaseModel):
    jobs: list[SampleJob] = LangChainField(required=True, description="list of jobs")


class CompanyInfo(LangChainBaseModel):
    countries: list[str] = LangChainField(required=False, description="List the countries where the company could be located, selecting from the <Country List>")
    minimum_headcount: Optional[int] = LangChainField(required=False, description="Determine the minimum number of employees the company employs. If not mentioned, try deduce this value if you can.")
    department_specific_headcount: dict[str, int] = LangChainField(required=False, description="Create a dictionary where the key is the department and the value is the minimum headcount for that department.")
    industries: list[str] = LangChainField(required=False, description="List the industries that match the description, selecting each from the <Industry List>.")
    funding_stages: list[str] = LangChainField(required=False, description="List the funding stages described, selecting each from the <Funding Stage List>.")
    annual_spend: Optional[int] = LangChainField(required=False, description="Estimate the minimum annual spend of the company or department in dollars.")
    software_tools: list[str] = LangChainField(required=False, description="List the software tools used by the company or department.")

    class Config:
        arbitrary_types_allowed = True
