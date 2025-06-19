from pydantic import BaseModel, Field
from typing import List, Optional

class ExcelHeaders(BaseModel):
    file1_columns: List[str]
    file2_columns: List[str]

class AuthenticationInput(BaseModel):
    value1: Optional[str]
    value2: Optional[str]
    column1: str
    column2: Optional[str]
    authentication_rule: str
    authentication_sub_rule: Optional[str]
