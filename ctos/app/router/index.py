from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.database.conn import db
from app.database.schema import Test
from app import models as m

from app.errors import exceptions as ex
from starlette.requests import Request
from fastapi.exceptions import HTTPException

router = APIRouter()

@router.get("/test/create/{name}", status_code=200)
async def create(name: str, session: Session = Depends(db.session)):
    rslt = Test().create(
        session
      , auto_commit=True
      , id=name
      , value=8000
      , err_txt="have no error")
    current_time = datetime.utcnow()
    return Response(f"""CTOS (UTC: {current_time.strftime('%Y-%m-%d %H:%M:%S')}""")

@router.get("/test/read/{id}", status_code=200, response_model=m.testMe)
async def read(id: str, session: Session = Depends(db.session)):
    rslt_arr = Test().read_one(id=id, session=session)
    return rslt_arr

@router.get("/test/read", status_code=200)#, response_model=list[m.testMe])
async def read(request: Request, session: Session = Depends(db.session)):
    rslt_arr = Test().read(session=session)
    raise ex.NoKeyMatchEx
    return rslt_arr


@router.get("/test/update/{name}", status_code=200)
async def update(name: str, session: Session = Depends(db.session)):
    all_data = Test().update(session
                  , auto_commit=True
                  , filter={"id" : name}
                  , update={"value" : 10000})
    return Response(f"""{all_data}""")

@router.get("/test/delete/{value}", status_code=200)
async def delete(value: str, session: Session = Depends(db.session)):
    all_data = Test().delete(session
                  , auto_commit=True
                  , value = value)
    return Response(f"""{all_data}""")

@router.get("/", status_code=200)
async def index():
    all_data = str(Test().all_columns()).replace(", Col", "\nCol")
    return Response(f"""{all_data}""")
