template = f'''
You are a recruiter and have rich experience on searching from Linkedin.com. 

I will provide you job position list(id, position).

Your task is to extract the best job functions and a job seniority of every item. Thus I can be search on Linkin.com based on the job functions and job security effectively.


Terminology
======
Job Function: 
Job Function refers to the specific role or set of responsibilities that an employee has within an organization. LinkedIn organizes job functions into various categories to help users and recruiters identify roles and responsibilities more effectively. Here’s a look into some of these job functions with examples.
- Software Engineer: Develops software applications.
- Marketing Manager: Plans and executes marketing strategies.
- Business Development Manager: Identifies growth opportunities.
- Financial Analyst: Analyzes financial data.
- Recruiter: Finds and hires candidates.
- Network Administrator: Manages network infrastructure.

Job Seniority:
Job Seniority indicates the level or rank of an employee within the organizational hierarchy. It typically represents the level of experience, responsibility, and authority the employee has. LinkedIn uses seniority levels to help users understand the career stage associated with a role. Common seniority levels include:
- Entry-Level: Little to no professional experience, basic tasks.
- Mid-Level: Moderate experience, more complex tasks.
- Senior-Level: High experience, leadership and decision-making.
- Manager: Manages teams or departments, oversees operations.
- Director: Senior management, strategic planning, and oversight.
- Executive: Top-level roles like CEO, COO, CFO, directing overall strategy and management.


job position list
======
15, Chairman and Chief Connectivity Officer (formerly Chief Collaboration Officer and CEO)
16, Founder, Online Dating Consultant
17, Operations Manager
18, Creator and Productivity Executive Coach

The output is a json list of dict, without any additional and markdown information.
item dict keys are: id:int, job_functions: list[str], job_seniority:str
'''


class ConnectionJobEnricher(object):
    def __init__(self):
        pass

    def enrich(self):
        pass
