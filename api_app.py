from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from civic_agents import CivicAgent
from civic_tasks import CivicTask
import os
from dotenv import load_dotenv
import uvicorn
from functools import lru_cache
from crewai import LLM, Crew
import logging

# Load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    print(f"Error loading .env file: {e}")

# Configure logging
try:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger(__name__)
except Exception as e:
    print(f"Error configuring logging: {e}")
    logger = logging.getLogger("fallback")

# Initialize FastAPI app with metadata
try:
    app = FastAPI(
        title="CivicNotice",
        description="A FastAPI-based backend service that streamlines the creation of professional Indian government public notices using AI agents.",
        version="0.0.1"
    )
except Exception as e:
    logger.error(f"Error initializing FastAPI app: {e}")
    raise

# Add CORS middleware to allow cross-origin requests
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
except Exception as e:
    logger.error(f"Error adding CORS middleware: {e}")
    raise

# Pydantic model for request body
class AnnouncementRequest(BaseModel):
    title: str = Field(..., description="Title of the public notice")
    body: str = Field(..., description="Body content of the public notice")
    date: str = Field(..., description="Date of the notice in DD/MM/YYYY format")
    location: str = Field(..., description="Location related to the notice")
    audience: str = Field(..., description="Target audience for the notice")
    category: str = Field(..., description="Category of the notice (e.g., maintenance, emergency, tender, etc.)")
    department: str = Field(..., description="Department responsible for the notice")
    contact_officer: str = Field(..., description="Name of the contact officer for the notice")
    contact_number: str = Field(..., description="Contact number for the notice")
    email: str = Field(..., description="Email address for the notice")
    additional_notes: Optional[str] = Field(None, description="Any additional notes or instructions for the notice")

# Pydantic model for response
class AnnouncementResponse(BaseModel):
    message: str
    error: Optional[str] = None

# Settings class to load environment variables
class Settings:
    def __init__(self):
        try:
            self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        except Exception as e:
            logger.error(f"Error loading GEMINI_API_KEY: {e}")
            self.GEMINI_API_KEY = None

# Cache settings for performance
@lru_cache()
def get_settings():
    try:
        return Settings()
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return None

# Main class to handle the crew logic
class CivicCrew():
    def __init__(self, title, body, date, location, audience, category, department, contact_officer, contact_number, email, additional_notes):
        try:
            self.title = title
            self.body = body
            self.date = date
            self.location = location
            self.audience = audience
            self.category = category
            self.department = department
            self.contact_officer = contact_officer
            self.contact_number = contact_number
            self.email = email
            self.additional_notes = additional_notes
            self.llm = LLM(model="gemini/gemini-2.5-flash")
            logger.info("CivicCrew initialized with title: %s", self.title)
        except Exception as e:
            logger.error(f"Error initializing CivicCrew: {e}")
            raise

    def run(self):
        try:
            logger.info("Starting the notice generation process.")
            agent = CivicAgent()
            task = CivicTask()

            # Create agents for generating and reviewing notices
            try:
                public_notice_generator = agent.public_notice_generator_agent()
                indian_notice_reviewer = agent.indian_notice_reviewer_agent()
            except Exception as e:
                logger.error(f"Error creating agents: {e}")
                raise

            # Create tasks for the crew
            try:
                generate_notice_task = task.generate_indian_notice_task(
                    agent=public_notice_generator,
                    title=self.title,
                    body=self.body,
                    date=self.date,
                    location=self.location,
                    audience=self.audience,
                    category=self.category,
                    department=self.department,
                    contact_officer=self.contact_officer,
                    contact_number=self.contact_number,
                    email=self.email,
                    additional_notes=self.additional_notes
                )
                review_notice_task = task.indian_notice_reviewer_task(agent=indian_notice_reviewer)
            except Exception as e:
                logger.error(f"Error creating tasks: {e}")
                raise

            # Assemble the crew with agents and tasks
            try:
                crew = Crew(
                    agents=[public_notice_generator, indian_notice_reviewer],
                    tasks=[generate_notice_task, review_notice_task],
                )
            except Exception as e:
                logger.error(f"Error assembling crew: {e}")
                raise

            logger.info("Crew assembled. Kicking off the workflow.")
            try:
                result = crew.kickoff()
            except Exception as e:
                logger.error(f"Error during crew kickoff: {e}")
                raise
            logger.info("Notice generation completed.")
            return result.raw
        except Exception as e:
            logger.error(f"Error in CivicCrew.run: {e}")
            raise

# Root endpoint for health check and docs link
@app.get("/")
async def root():
    try:
        logger.info("Root endpoint accessed.")
        return {
            "message": "Welcome to the CivicNotice API! This service helps you create professional Indian government public notices using AI agents.",
            "docs": "/docs"
        }
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to generate a public notice
@app.post("/generate_notice", response_model=AnnouncementResponse)
async def generate_notice(request: AnnouncementRequest):
    logger.info("Received request to generate notice: %s", request.title)
    try:
        civic_crew = CivicCrew(
            title=request.title,
            body=request.body,
            date=request.date,
            location=request.location,
            audience=request.audience,
            category=request.category,
            department=request.department,
            contact_officer=request.contact_officer,
            contact_number=request.contact_number,
            email=request.email,
            additional_notes=request.additional_notes
        )
        try:
            result = civic_crew.run()
        except Exception as e:
            logger.error("Error running CivicCrew: %s", str(e))
            return AnnouncementResponse(message="", error=str(e))
        logger.info("Notice generated successfully for title: %s", request.title)
        return AnnouncementResponse(message=result, error=None)
    except Exception as e:
        logger.error("Error generating notice: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))

# Run the app if executed directly
if __name__ == "__main__":
    try:
        logger.info("Starting CivicNotice API server.")
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Error starting server: {e}")