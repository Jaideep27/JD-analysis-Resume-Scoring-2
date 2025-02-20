import json
from typing import Dict, List
from fastapi import HTTPException
import google.generativeai as genai
from models.config import Config
from dotenv import load_dotenv
import os

Config.initialize()
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

class ResumeScorer:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro")

    def create_detailed_prompt(self, text: str, criteria_list: List[str]) -> str:
        formatted_criteria = "\n".join(f"- {criterion}" for criterion in criteria_list)
        return f"""
        You are an expert HR professional with extensive experience in technical hiring. 
        Evaluate this resume against each criterion on a scale of 0-5.
        
        Scoring Guidelines:
        5 - Exceptional match
        4 - Strong match
        3 - Good match
        2 - Fair match
        1 - Poor match
        0 - No match
        
        Criteria to evaluate:
        {formatted_criteria}
        
        Resume Text:
        {text}
        
        Please provide the scores for each criterion in this exact format (maintain exact criterion names):
        {{
            {', '.join(f'"{criterion}": <score>' for criterion in criteria_list)}
        }}
        """

    def validate_score(self, score: int) -> int:
        return max(0, min(Config.MAX_SCORE, score))

    def parse_scores(self, response_text: str, criteria_list: List[str]) -> Dict[str, int]:
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:-3].strip()
            
            # Parse the JSON response
            scores = json.loads(cleaned_text)
            
            # Create a dictionary with validated scores for each criterion
            validated_scores = {}
            for criterion in criteria_list:
                score = scores.get(criterion, 0)
                validated_scores[criterion] = self.validate_score(int(float(score)))
            
            return validated_scores
        except Exception as e:
            print(f"Error parsing scores: {e}")
            return {criterion: 0 for criterion in criteria_list}

    def score_resume(self, text: str, criteria_list: List[str]) -> Dict[str, int]:
        try:
            prompt = self.create_detailed_prompt(text, criteria_list)
            response = self.model.generate_content(prompt)
            if not response.text:
                raise ValueError("Empty response from model")
            return self.parse_scores(response.text, criteria_list)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scoring error: {str(e)}")