from crewai import Task
from dotenv import load_dotenv

load_dotenv()

class CivicTask():

    def generate_indian_notice_task(self,agent,title,body,date,location,audience,category,department,contact_officer,contact_number,email,additional_notes):
        return Task(
            description=f'''
            Generate a professional Indian government public notice based on the following input:
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
            5. Use formal yet accessible language
            6. Include proper contact information
            7. Follow category-specific formatting
            8. Ensure cultural sensitivity and respect
            9. Include government seal/signature line
            
            ''',
            expected_output='A complete, professionally formatted Indian government public notice ready for review',
            agent=agent
        )
    
    def indian_notice_reviewer_task(self,agent):
        return Task(
        description='''
        Review the generated Indian government public notice and ensure it meets all official standards:
        
        1. Validate using Indian notice validation tool
        2. Check compliance with Indian government communication standards
        3. Verify RTI compliance and transparency requirements
        4. Ensure proper bilingual formatting (if applicable)
        5. Check cultural sensitivity and appropriate tone
        6. Verify all required contact information is included
        7. Ensure proper authority designation and signatures
        8. Check date format (DD/MM/YYYY)
        9. Verify department/authority credentials
        10. Ensure accessibility for diverse Indian population
        
        Indian Government Specific Checks:
        - Proper use of government letterhead format
        - Inclusion of reference number (if applicable)
        - Appropriate use of official language
        - Compliance with Right to Information Act
        - Proper grievance redressal mechanism mention
        
        If the notice needs improvements:
        - Provide specific feedback based on Indian government standards
        - Suggest culturally appropriate revisions
        - Ensure compliance with Indian administrative protocols
        
        If the notice meets all standards:
        - Mark it as approved for official publication
        - Provide final formatted version with all required elements
        ''',
        expected_output='Either an approved final Indian government notice or specific feedback for revision',
        agent=agent
    )