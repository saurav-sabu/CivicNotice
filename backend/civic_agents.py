import logging
from crewai import Agent, LLM
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logger for this module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CivicAgent():
    def __init__(self):
        # Initialize the LLM model for use by agents
        self.llm = LLM(model="gemini/gemini-2.5-flash")
        logger.info("Initialized CivicAgent with LLM model: gemini/gemini-2.5-flash")

    def public_notice_generator_agent(self):
        """
        Creates and returns an Agent specialized in generating public notices
        compliant with Indian government standards and RTI guidelines.
        """
        logger.info("Creating Public Notice Generator Agent")
        return Agent(
            role="Public Notice Generator",
            goal="Generate clear, structured public notices in the specified language that meet Indian government standards and RTI compliance requirements, formatted in markdown",
            backstory='''You are an expert in Indian government communication standards and public announcement protocols. 
            You specialize in creating official notices that comply with Indian bureaucratic formats, and 
            accessibility standards. You understand and follow proper government formatting conventions. 
            You are familiar with various Indian government notice types including maintenance, emergency, tender, tax, recruitment, and public meeting notices. 
            You generate only the final notice content in the requested language formatted in markdown without any explanatory text or feedback.''',
            verbose=False,
            allow_delegation=True,
            llm=self.llm
        )
    
    def indian_notice_reviewer_agent(self):
        """
        Creates and returns an Agent specialized in reviewing and approving
        notices for compliance with Indian government and RTI standards.
        """
        logger.info("Creating Indian Government Notice Reviewer & Compliance Officer Agent")
        return Agent(
            role="Indian Government Notice Reviewer & Compliance Officer",
            goal='Review and finalize notices in the specified language ensuring compliance with Indian government standards, RTI guidelines, and provide only the final approved notice in markdown format without any feedback or comments',
            backstory='''You are a seasoned Indian government communications reviewer with expertise in 
            official communication protocols, and public messaging standards. You ensure all notices meet Central/State 
            government requirements in the specified language, and maintain the dignity and authority expected in government communications. 
            You have experience with various government departments and understand the nuances of Indian administrative communication. 
            You provide only the final approved notice in the requested language formatted in markdown without any review comments or feedback.''',
            verbose=False,
            allow_delegation=False,
            llm=self.llm
        )