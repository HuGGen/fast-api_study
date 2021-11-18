from dataclasses import asdict
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends

from app.router import index, auth

from app.database.conn import db
from app.common.config import conf
from app.middlewares.token_validator import access_control

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from app.middlewares.basemiddleware import CheckApiKey

def create_app():
    com_conf = conf()
    app = FastAPI()
    conf_dict = asdict(com_conf)
    db.init_app(app, **conf_dict)

    app.add_middleware(CheckApiKey)
    #app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(CORSMiddleware, **conf().CORS_OPTIONS)
    app.add_middleware(TrustedHostMiddleware, **conf().TRUSTED_HOSTS_OPTIONS)

    app.include_router(index.router)
    app.include_router(auth.router, prefix="/api", tags=["users"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app"
              , host="0.0.0.0"
              , port=8000
              , reload=conf().PROJ_RELOAD)

