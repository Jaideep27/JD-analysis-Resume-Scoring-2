from enum import Enum

class CriteriaType(str, Enum):
    overall = "overall"
    skills = "skills"
    experience = "experience"
    certifications = "certifications"
    qualifications = "qualifications"
    education = "education"
    tools = "tools"
    languages = "languages"
    responsibilities = "responsibilities"
    benefits = "benefits"
    culture = "company culture"