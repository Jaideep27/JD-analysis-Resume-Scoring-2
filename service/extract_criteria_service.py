import os
import pdfplumber
import docx
from models.criteria_type import CriteriaType
import google.generativeai as genai
from fastapi import File, HTTPException, Query, UploadFile
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {str(e)}")
    
    
def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from DOCX: {str(e)}")


def extract_key_criteria(text, criteria_type):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Handle 'overall' criteria type specially
        if criteria_type == 'overall':
            prompt = f"""
            Extract key ranking criteria (skills, experience, certifications, qualifications) 
            from the following job description.:
    
            {text}
            """
        else:
            prompt = f""" 
            Extract key criteria related to {criteria_type}  
            from the following job description. Return them as a list.
            Only include the actual criteria without any explanatory text or headings:

            {text} 
            """
        
        response = model.generate_content(prompt)
        
        # Process the response to get clean criteria items
        criteria_lines = [line.strip() for line in response.text.split("\n") if line.strip()]
        
        # Remove numbering and any extra spaces
        cleaned_criteria = []
        for line in criteria_lines:
            # Remove numbering (1., 2., etc.)
            if line[0].isdigit() and line[1:].startswith('. '):
                line = line[line.find('.')+1:].strip()
            # Remove bullet points if present
            if line.startswith('• '):
                line = line[2:].strip()
            if line.startswith('- '):
                line = line[2:].strip()
            if line:
                cleaned_criteria.append(line)
                
        return cleaned_criteria
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting criteria using Gemini: {str(e)}")


async def extract_criteria(
        file: UploadFile = File(...),
        criteria_type: CriteriaType = Query()
):
    try:
        file_path = f"./temp/{file.filename}"

        os.makedirs("./temp", exist_ok=True)

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:  # .docx
            text = extract_text_from_docx(file_path)

        if not text or text.isspace():
            raise HTTPException(status_code=422, detail="Could not extract any text from the provided file. Please check the file content.")

        criteria_type_str = criteria_type.value

        criteria = extract_key_criteria(text, criteria_type_str)

        if not criteria:
            raise HTTPException(status_code=404, detail="No criteria could be extracted from the provided document.")
        
        return {
            "criteria": criteria,
            "criteria_type": criteria_type_str
        }
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No criteria could be extracted from the provided document.{str(e)}")
