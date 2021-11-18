from pydantic.main import BaseModel

class testMe(BaseModel):
    value:int = None
    err_txt:str = None
    id:str = None

    class Config:
        orm_mode = True