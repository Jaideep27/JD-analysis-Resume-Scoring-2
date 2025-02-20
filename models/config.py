import os

class Config:
    UPLOAD_DIR = "temp/uploads"
    OUTPUT_DIR = "temp/output"
    ALLOWED_EXTENSIONS = {".pdf", ".docx"}
    MAX_SCORE = 5

    @classmethod
    def initialize(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)