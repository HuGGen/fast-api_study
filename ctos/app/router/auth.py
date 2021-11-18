from fastapi import APIRouter

from app.errors import exceptions as ex
from starlette.requests import Request

router = APIRouter()

@router.get("/auth", status_code=200)
async def create(request: Request):
    raise ex.SqlFailureEx()
    return "Hello World!"
