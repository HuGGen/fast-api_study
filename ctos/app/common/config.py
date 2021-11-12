from dataclasses import dataclass, asdict
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
    DB_URL: str = environ.get("DB_URL", "postgresql://pgadmin:pgadmin@192.168.56.1:5432/postgres")

@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    PROJ_RELOAD: bool = True

@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    PROJ_RELOAD: bool = False

def conf():
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))

