from datetime import datetime
import os
import shutil
import pandas as pd
from fastapi import File, Form, HTTPException, UploadFile
from typing import List
from models.resume_scorer import ResumeScorer
from models.text_extractor import TextExtractor
from models.config import Config
import google.generativeai as genai
from dotenv import load_dotenv

Config.initialize()

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=GEMINI_API_KEY)


async def score_resume(files: List[UploadFile] = File(...),
                       criteria: str = Form(...)):
    try:
        if not criteria or not files:
            raise HTTPException(status_code=400, detail="Both criteria and files are required")
    
        criteria_list = [c.strip() for c in criteria.split(',')]

        scorer = ResumeScorer()

        results = []

        for file in files:
            if os.path.splitext(file.filename)[1].lower() not in Config.ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(Config.UPLOAD_DIR, file.filename)
            try:
                # Save and process file
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                # Extract text and get scores
                text = TextExtractor.extract_text(file_path)
                scores = scorer.score_resume(text, criteria_list)

                # Create result row with individual scores
                row = {
                    "Candidate Name": os.path.splitext(file.filename)[0]
                }
                
                # Add each criterion score separately
                for criterion in criteria_list:
                    row[criterion] = scores[criterion]
                
                # Add total score
                row["Total Score"] = sum(scores.values())
                
                results.append(row)

            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

        if not results:
            raise HTTPException(status_code=500, detail="No files were processed successfully")
    
        df = pd.DataFrame(results)
    
        # Ensure columns are in the correct order
        columns = ["Candidate Name"] + criteria_list + ["Total Score"]
        df = df.reindex(columns=columns)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"resume_scores_{timestamp}.csv"
        output_path = os.path.join(Config.OUTPUT_DIR, output_filename)
        
        # Save to CSV with each criterion as a separate column
        df.to_csv(output_path, index=False)

        return{
            "message": "Processing complete",
            "file_url": f"/download/{output_filename}",
            "total_processed": len(results),
            "timestamp": datetime.now().isoformat(),
        }
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No criteria could be extracted from the provided document.{str(e)}")

        