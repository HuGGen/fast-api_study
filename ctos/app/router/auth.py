from fastapi import APIRouter


router = APIRouter()

@router.get("/auth", status_code=200)
async def create():
    return "Hello World!"
