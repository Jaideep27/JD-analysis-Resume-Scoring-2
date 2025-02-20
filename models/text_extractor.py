import os
import docx
from fastapi import HTTPException
import pdfplumber


class TextExtractor:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error extracting PDF: {str(e)}"
            )

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error extracting DOCX: {str(e)}"
            )

    @classmethod
    def extract_text(cls, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return cls.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return cls.extract_text_from_docx(file_path)
        else:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file format: {ext}"
            )