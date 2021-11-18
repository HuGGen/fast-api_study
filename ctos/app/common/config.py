from dataclasses import dataclass, asdict, field
from os import path, environ
from typing import List

base_dir = path.dirname(\
                    path.dirname(\
                        path.abspath(__file__)))

@dataclass
class Config:
    BASE_DIR = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    TEST_MODE: bool = False

@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True

    ##--CORS OPTIONS [Dev]
    CORS_OPTIONS = {
        "allow_origins"     : ["*"],
        "allow_credentials" : True,
        "allow_methods"     : ["*"],
        "allow_headers"     : ["*"],
    }
    ##--TRUSTED HOSTS OPTIONS [Dev]
    TRUSTED_HOSTS_OPTIONS = {
        "allowed_hosts" : ["*"],
        "except_path"   : ["/"]
    }

    ##--DB URL [Dev]
    DB_URL: str = environ.get("DB_URL", "postgresql://postgres:postgres@132.226.20.151:5432/postgres")


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False

    ##--CORS OPTIONS [Prd]
    CORS_OPTIONS = {
        "allow_origins"     : ["*"],
        "allow_credentials" : False,
        "allow_methods"     : ["*"],
        "allow_headers"     : ["*"],
    }
    ##--TRUSTED HOSTS OPTIONS [Prd]
    TRUSTED_HOSTS_OPTIONS = {
        "allowed_hosts" : ["*"],
        "except_path"   : ["/"]
    }

    ##--DB URL [Prd]
    DB_URL: str = environ.get("DB_URL", "postgresql://postgres:postgres@132.226.20.151:5432/postgres")


def conf():
    config = dict(prd=ProdConfig(), dev=LocalConfig())
    return config.get(environ.get("API_ENV", "dev"))

