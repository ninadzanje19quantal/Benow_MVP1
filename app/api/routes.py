# libraries
from fastapi import FastAPI, Query, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from enum import Enum
from pydantic import BaseModel, Field
import io
import pandas as pd
import numpy as np
import json
import re

# files1
from app.services.llm_service import *
from app.services.file_processing import *
from app.services.authentication import *

# initialize the App
benow_app = FastAPI()

final_matched_columns: dict = {}
excel_file1 = pd.DataFrame()
excel_file2 = pd.DataFrame()

validation_list = [
    "greater than",
    "less than",
    "equal to",
    "not equal to"
]

exception = []


# uvicorn backend_endpoints:benow_app --reload

class excel_headers(BaseModel):
    file1_columns: list
    file2_columns: list


# basic route structure
@benow_app.get("/")
async def home():
    return {"Hello": "World"}


"""@benow_app.get("/get_recon_of_company")
async def get_recon_of_company_fapi(company_name: str):
    company_recon = get_recon_by_name(company_name)
    return company_recon


@benow_app.get("/get_all_recons")
async def get_all_recons_fapi():
    all_recons = get_all_recons()
    return all_recons"""


@benow_app.post("/create-recon")
async def create_recon(recon_name: str = ...,
                       file1: UploadFile = File(...),
                       file2: UploadFile = File(...)):
    global excel_file1, excel_file2

    # Read the uploaded Excel files into DataFrames
    excel_file1 = pd.read_excel(io.BytesIO(file1.file.read()))
    excel_file2 = pd.read_excel(io.BytesIO(file2.file.read()))

    headers = get_headers(excel_file1, excel_file2)

    return headers


@benow_app.post("/automatch")
async def automatch(columns: excel_headers):
    matched_headers = match_headers(columns.file1_columns, columns.file2_columns)
    return matched_headers


@benow_app.post("/intelligence-engine/")
async def intelligence_engine(
        file1: UploadFile = File(...),
        file2: UploadFile = File(...),
        primary_key: str = Query(None, min_length=3, max_length=10, title="Primary Key",
                                 description="Enter type primary key", alias="item-query")
):
    # Read the uploaded Excel files into DataFrames
    file1 = pd.read_excel(io.BytesIO(file1.file.read()))
    file2 = pd.read_excel(io.BytesIO(file2.file.read()))

    file1_columns = file1.columns.tolist()
    file2_columns = file2.columns.tolist()

    matched_headers = match_headers(file1_columns, file2_columns)

    return type(file1)


@benow_app.post("/manual-mapping")
async def manual_mapping(user_matched_columns: dict) -> dict:
    final_matched_columns = user_matched_columns
    return final_matched_columns


@benow_app.post("/validations")
async def validations(primary_key: str = Query(None, min_length=3, max_length=1000, title="Primary Key",
                                               description="Enter type primary key. (file1_column:file2_column)"),
                      validation: str = Query(..., min_length=3, max_length=1000, title="Validation Rule",
                                              description="Enter the validation rule"),
                      field1: str = (...), field2: str = (...)):
    primary_key = primary_key.split(":")

    field1_data = excel_file1[field1].tolist()
    field2_data = excel_file2[field2].tolist()

    if validation == "greater than":
        for i, j in zip(field1_data, field2_data):
            if i > j:
                exception.append((i, j))

    elif validation == "less than":
        for i, j in zip(field1_data, field2_data):
            if i > j:
                exception.append((i, j))

    elif validation == "equal to":
        for i, j in zip(field1_data, field2_data):
            if i == j:
                exception.append((i, j))

    elif validation == "not equal to":
        for i, j in zip(field1_data, field2_data):
            if i != j:
                exception.append((i, j))

    return {"Exception": exception}

class authentication(BaseModel):
    value1: str | None = Field(None, title="Value")
    value2: str | None = Field(None, title="Value")
    column1: str = Field(..., title="Column", description="Enter the name of the column")
    column2: str | None = Field(None, title="Column", description="Enter the name of the column")
    authentication_rule: str  = Field(..., title="Validation Rule", description="Enter the name of the Validation rule")
    authentication_sub_rule: str | None = Field(..., title="Validation Sub Rule", description="Enter the name of the Validation Sub Rule")


@benow_app.post("/authenticate")
async def authenticate(authentication_obj: authentication, user_validation):
    auth_fail = []
    field1_data = excel_file1[authentication_obj.column1].tolist()
    if authentication_obj.column2:
        field2_data = excel_file2[authentication_obj.column2].tolist()


    if authenticate == "length of the field":
        for data in field1_data:
            if len(data) == authentication_obj.value1:
                pass
            else:
                matches = np.where(excel_file1 == data)
                auth_fail.extend([(int(row), int(col)) for row, col in zip(*matches)])

    elif authenticate == "text format - alphabets":
        for data in field1_data:
            if str(data).isalpha():
                pass
            else:
                matches = np.where(excel_file1 == data)
                auth_fail.extend([(int(row), int(col)) for row, col in zip(*matches)])

    elif authenticate == "text format - numeric":
        for data in field1_data:
            if str(data).isdigit():
                pass
            else:
                matches = np.where(excel_file1 == data)
                auth_fail.extend([(int(row), int(col)) for row, col in zip(*matches)])

    elif authenticate == "text format - alphanumeric":
        for data in field1_data:
            if str(data).isalnum():
                pass
            else:
                matches = np.where(excel_file1 == data)
                auth_fail.extend([(int(row), int(col)) for row, col in zip(*matches)])

    elif authenticate == "text format - special characters":
        for data in field1_data:
            if bool(re.search(r'[^a-zA-Z0-9]', str(data))):
                pass
            else:
                matches = np.where(excel_file1 == data)
                auth_fail.extend([(int(row), int(col)) for row, col in zip(*matches)])

    elif authenticate == "field value >":
        for data in field1_data:
            try:
                if float(data) > float(authentication_obj.value1):
                    pass
                else:
                    matches = np.where(excel_file1 == data)
                    auth_fail.extend([(int(row), int(col)) for row, col in zip(*matches)])
            except:
                continue
    elif authenticate == "field value <":
        for data in field1_data:
            try:
                if float(data) < float(authentication_obj.value1):
                    pass
                else:
                    matches = np.where(excel_file1 == data)
                    auth_fail.extend([(int(row), int(col)) for row, col in zip(*matches)])
            except:
                continue

    return {"Failed Authentications": auth_fail}