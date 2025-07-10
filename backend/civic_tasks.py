from crewai import Task
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class CivicTask():
    """
    Class to generate and review Indian government public notices.
    """

    def generate_indian_notice_task(
        self, agent, title, body, date, location, audience, language, category,
        department, contact_officer, contact_number, email, additional_notes
    ):
        """
        Creates a Task for generating a professional Indian government public notice.
        """
        logger.info("Generating Indian government public notice task with title: %s in language: %s", title, language)
        
        # Prepare the Task object with detailed instructions and expected output
        task = Task(
            description=f'''
            Generate a professional Indian government public notice in {language} based on the following input:
            - Title: {title}
            - Body: {body}
            - Date: {date}
            - Location: {location}
            - Audience: {audience}
            - Language: {language}
            - Category: {category}
            - Department: {department}
            - Contact Officer: {contact_officer}
            - Contact Number: {contact_number}
            - Email: {email}
            - Additional Notes: {additional_notes}
            
            Create a notice that follows Indian government standards:
            1. Use appropriate government letterhead format
            2. Include proper authority designation
            3. Follow Indian date format (DD/MM/YYYY)
            4. Use formal language appropriate for the specified language
            5. Include proper contact information
            6. Follow category-specific formatting
            7. Ensure cultural sensitivity and respect
            8. Include government seal/signature line
            9. Format the entire notice in markdown
            
            IMPORTANT: Provide ONLY the final formatted notice content in {language} using markdown format. Do not include any explanatory text, comments, or additional information.
            ''',
            expected_output=f'A complete, professionally formatted Indian government public notice in {language} using markdown format, ready for publication (notice content only, no explanations)',
            agent=agent
        )
        logger.info("Task for generating notice in %s created successfully.", language)
        return task

    def indian_notice_reviewer_task(self, agent, language):
        """
        Creates a Task for reviewing an Indian government public notice.
        """
        logger.info("Creating Indian government public notice reviewer task for language: %s", language)
        
        # Prepare the Task object with review instructions and expected output
        task = Task(
            description=f'''
            Review the generated Indian government public notice in {language} and ensure it meets all official standards:
            
            General Compliance Checks:
            1. Check compliance with Indian government communication standards
            2. Ensure proper formatting for the specified language
            3. Check cultural sensitivity and appropriate tone
            4. Verify all required contact information is included
            5. Ensure proper authority designation and signatures
            6. Check date format (DD/MM/YYYY)
            7. Verify department/authority credentials
            8. Ensure accessibility for diverse Indian population
            9. Ensure the notice is properly formatted in markdown
            
            Indian Government Specific Checks:
            - Proper use of government letterhead format
            - Inclusion of reference number (if applicable)
            - Appropriate use of official language as specified
            - Proper grievance redressal mechanism mention
            - Ensure markdown formatting is consistent and readable
            
            IMPORTANT: Provide ONLY the final approved notice in {language} using markdown format. Do not provide any feedback, comments, 
            suggestions, or explanatory text. Only output the complete, final formatted notice ready for publication.
            ''',
            expected_output=f'Final approved Indian government notice in {language} formatted in markdown (notice content only, no feedback or comments)',
            agent=agent
        )
        logger.info("Reviewer task for %s created successfully.", language)
        return task