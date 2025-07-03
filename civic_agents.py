from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

class CivicAgent():

    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash")

    def public_notice_generator_agent(self):
        return Agent(
            role = "Public Notice Generator",
            goal = "Generate clear, structured public notices from user input that meet the Indian government standards of India and RTI Compliance",
            backstory='''You are an expert in Indian government communication standards and public announcement protocols. 
            You specialize in creating official notices that comply with Indian bureaucratic formats, RTI guidelines, and 
            accessibility standards. You understand follow proper government formatting conventions. You are familiar with various Indian government notice types 
            including maintenance, emergency, tender, tax, recruitment, and public meeting notices.''',
            verbose = False,
            allow_delegation = False,
            llm = self.llm
        )
    
    def indian_notice_reviewer_agent(self):
        return Agent(
            role = "Indian Government Notice Reviewer & Compliance Officer",
            goal='Review and approve notices ensuring compliance with Indian government standards, RTI guidelines, and accessibility requirements',
            backstory='''You are a seasoned Indian government communications reviewer with expertise in RTI compliance, 
            official communication protocols, and public messaging standards. You ensure all notices meet Central/State 
            government requirements, follow proper bilingual formatting when needed, and maintain the dignity and 
            authority expected in government communications. You have experience with various government departments 
            and understand the nuances of Indian administrative communication.''',
            verbose = False,
            allow_delegation = False,
            llm = self.llm
        )