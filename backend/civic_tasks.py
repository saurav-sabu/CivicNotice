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
        self, agent, title, body, date, location, audience, category,
        department, contact_officer, contact_number, email, additional_notes
    ):
        """
        Creates a Task for generating a professional Indian government public notice.
        """
        logger.info("Generating Indian government public notice task with title: %s", title)
        # Prepare the Task object with detailed instructions and expected output
        task = Task(
            description=f'''
            Generate a professional Indian government public notice in English only based on the following input:
            - Title: {title}
            - Body: {body}
            - Date: {date}
            - Location: {location}
            - Audience: {audience}
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
            4. Include RTI compliance note
            5. Use formal yet accessible English language
            6. Include proper contact information
            7. Follow category-specific formatting
            8. Ensure cultural sensitivity and respect
            9. Include government seal/signature line
            
            IMPORTANT: Provide ONLY the final formatted notice content. Do not include any explanatory text, comments, or additional information.
            ''',
            expected_output='A complete, professionally formatted Indian government public notice in English ready for publication (notice content only, no explanations)',
            agent=agent
        )
        logger.info("Task for generating notice created successfully.")
        return task

    def indian_notice_reviewer_task(self, agent):
        """
        Creates a Task for reviewing an Indian government public notice.
        """
        logger.info("Creating Indian government public notice reviewer task.")
        # Prepare the Task object with review instructions and expected output
        task = Task(
            description='''
            Review the generated Indian government public notice and ensure it meets all official standards:
            
            1. Check compliance with Indian government communication standards
            2. Verify RTI compliance and transparency requirements
            3. Ensure proper English language formatting
            4. Check cultural sensitivity and appropriate tone
            5. Verify all required contact information is included
            6. Ensure proper authority designation and signatures
            7. Check date format (DD/MM/YYYY)
            8. Verify department/authority credentials
            9. Ensure accessibility for diverse Indian population
            
            Indian Government Specific Checks:
            - Proper use of government letterhead format
            - Inclusion of reference number (if applicable)
            - Appropriate use of official English language
            - Compliance with Right to Information Act
            - Proper grievance redressal mechanism mention
            
            IMPORTANT: Provide ONLY the final approved notice in English. Do not provide any feedback, comments, 
            suggestions, or explanatory text. Only output the complete, final formatted notice ready for publication.
            ''',
            expected_output='Final approved Indian government notice in English (notice content only, no feedback or comments)',
            agent=agent
        )
        logger.info("Reviewer task created successfully.")
        return task