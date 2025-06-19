from fastapi import APIRouter, UploadFile, File, Query
from app.services import file_processing, authentication, llm_service
from app.models.schemas import ExcelHeaders, AuthenticationInput

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Benow Backend is up!"}

@router.post("/create-recon")
async def create_recon(recon_name: str, file1: UploadFile = File(...), file2: UploadFile = File(...)):
    df1, df2 = file_processing.read_files(file1, file2)
    return file_processing.get_headers(df1, df2)

@router.post("/automatch")
async def auto_match(columns: ExcelHeaders):
    return llm_service.match_headers(columns.file1_columns, columns.file2_columns)

@router.post("/authenticate")
async def authenticate_user(input: AuthenticationInput, rule: str):
    return authentication.run_authentication(input, rule)
