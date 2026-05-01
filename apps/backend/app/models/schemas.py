from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CVUploadResponse(BaseModel):
    message: str
    cv_id: str
    extracted_text: str

class AnalysisRequest(BaseModel):
    cv_id: str
    job_description: str

class ResourceItem(BaseModel):
    title: str = ""
    url: str = ""
    engine: str = ""

class RoadmapDay(BaseModel):
    day: int = 0
    topic: str = ""
    description: str = ""
    search_query: str = ""
    resources: Optional[List[ResourceItem]] = Field(default_factory=list)

class Roadmap(BaseModel):
    days: List[RoadmapDay] = Field(default_factory=list)

class ProjectItem(BaseModel):
    name: str = ""
    link: str = ""
    description: str = ""
    stack: str = ""

class EduItem(BaseModel):
    degree: str = ""
    school: str = ""
    date_range: str = ""
    gpa: str = ""

class AIAnalysisResponse(BaseModel):
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    github_username: str = ""
    job_title: str = ""
    skills_tools: str = ""
    skills_automation: str = ""
    skills_ai_dev: str = ""
    skills_other: str = ""
    faked_skills: List[str] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    education: List[EduItem] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    match_score_before: int = 0
    match_score_after: int = 0
    roadmap: Roadmap = Field(default_factory=lambda: Roadmap(days=[]))

    class Config:
        extra = "ignore"

class CompileRequest(BaseModel):
    analysis: AIAnalysisResponse
    cv_id: str = ""
    template_name: str = "classic.tex"
    
    class Config:
        extra = "ignore"
