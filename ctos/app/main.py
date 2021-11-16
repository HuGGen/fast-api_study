from dataclasses import asdict
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends

from app.router import index, auth

from app.database.conn import db
from app.common.config import conf

from starlette.middleware.cors import CORSMiddleware
from app.middlewares.trusted_hosts import TrustedHostMiddleware

def create_app():
    com_conf = conf()
    app = FastAPI()
    conf_dict = asdict(com_conf)
    db.init_app(app, **conf_dict)
    app.add_middleware(CORSMiddleware
                       , allow_origins=["https://localhost:8000"]#conf().ALLOW_SITE
                       , allow_credentials=True
                       , allow_methods=["*"] # POST, GET, PUT, DELETE
                       , allow_headers=["*"]) #"Content-Type"

    app.add_middleware(TrustedHostMiddleware
                       , allowed_hosts=conf().TRUSTED_HOSTS
                       , except_path=["/"])

    app.include_router(index.router)
    app.include_router(auth.router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app"
              , host="0.0.0.0"
              , port=8000
              , reload=conf().PROJ_RELOAD)