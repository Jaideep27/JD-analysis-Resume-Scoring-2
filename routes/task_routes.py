import os
from typing import List
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from models.config import Config
from models.criteria_type import CriteriaType
from service.extract_criteria_service import extract_criteria
from service.score_resume_service import score_resume

task_router = APIRouter()

@task_router.post("/extract_criteria")
async def _extract_criteria(
    file: UploadFile = File(...),
    criteria_type: CriteriaType = Query(default=CriteriaType.overall)
):

    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a PDF or DOCX file.")
    
    response = await extract_criteria(file=file,criteria_type=criteria_type)

    return response



@task_router.post("/score_resume")
async def _score_resume(
    files: List[UploadFile] = File(...),
    criteria: str = Form(...)
):
    response = await score_resume(files=files,criteria=criteria)

    return response


@task_router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(Config.OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)