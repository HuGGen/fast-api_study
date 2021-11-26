from fastapi import APIRouter, Depends, File, UploadFile

from app.errors import exceptions as ex
from starlette.requests import Request

from sqlalchemy.orm import Session
from app.database.schema import Test
from app.database.conn import db

from app import models as m
from typing import List

from io import BytesIO
import pandas as pd

router = APIRouter()

@router.get("/auth", status_code=200)
async def create(request: Request):
    raise ex.SqlFailureEx()
    return "Hello World!"

@router.get("/services", status_code=200, response_model=list[m.testMe])
async def chk_apiKey(request: Request, session : Session = Depends(db.session)):
    sess = next(db.session()) if not session else session
    result = sess.query(Test).filter(Test.id.in_(["aaa", "ccc"])).all()
    return result

@router.post("/files", status_code=200)
async def file(request: Request, files: bytes = File(...)):
    csv_file = pd.read_csv(BytesIO(files), encoding="cp949", sep='\t')
    return csv_file.to_json()