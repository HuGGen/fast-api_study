from pydantic.main import BaseModel

class queryReturnModel(BaseModel):
    class Config:
        orm_mode = True

class testMe(queryReturnModel):
    value:int = None
    err_txt:str = None
    id:str = None
