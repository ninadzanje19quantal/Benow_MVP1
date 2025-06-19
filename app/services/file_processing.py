import pandas as pd
import io

def read_files(file1, file2):
    df1 = pd.read_excel(io.BytesIO(file1.file.read()))
    df2 = pd.read_excel(io.BytesIO(file2.file.read()))
    return df1, df2

def get_headers(df1: pd.DataFrame, df2: pd.DataFrame) -> dict:
    return {"file1": list(df1.columns), "file2": list(df2.columns)}
