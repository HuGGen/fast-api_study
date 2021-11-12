from dataclasses import asdict
#from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends

from app.common.config import conf
from app.database.conn import db
from app.router import index

def create_app():
    com_conf = conf()
    app = FastAPI()
    conf_dict = asdict(com_conf)
    db.init_app(app, **conf_dict)

    app.include_router(index.router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app"
              , host="0.0.0.0"
              , port=8000
              , reload=conf().PROJ_RELOAD)