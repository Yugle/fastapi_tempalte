import os
from pydantic import BaseSettings, BaseModel
from fastapi import Query
from typing import Optional, List
from loguru import logger
import json
import yaml


class Settings(BaseSettings):
    config_file: Optional[str] = 'conf/config.yaml'
    log_path: Optional[str] = 'logs'


class HTTPConfig(BaseModel):
    port: str = Query(..., min_length=1, regex=r'^\d+$')


class DatabaseConfig(BaseModel):
    host: str = Query(..., min_length=1)
    port: str = Query(..., min_length=1)
    username: str = Query(..., min_length=1)
    password: str = Query(..., min_length=1)
    db_name: str = Query(..., min_length=1)


class SSOConfig(BaseModel):
    url_to_get_token: str = Query(..., min_length=1)
    client_id: str = Query(..., min_length=1)
    redirect_uri: str = Query(..., min_length=1)
    grant_type: str = Query(..., min_length=1)


class JWTConfig(BaseModel):
    secret_key: str = Query(..., min_length=1)
    algorithm: str = Query(..., min_length=1)
    access_token_expire_minutes: str = Query(..., min_length=1)


IgnoreAuthUrlsConfig = List[str]


class Config(BaseModel):
    sql_server: DatabaseConfig
    mongo: DatabaseConfig
    http: HTTPConfig
    sso: SSOConfig
    jwt: JWTConfig
    ignore_auth_urls: IgnoreAuthUrlsConfig

    def __str__(self) -> str:
        return json.dumps(self.dict(), indent=2)


def check_yaml(cfg):
    config = Config.parse_obj(cfg)
    logger.debug(f'config: {config}')

    return True


settings = Settings()
logger.debug(f'settings: {settings.json()}')

try:
    config = Config(**yaml.safe_load(open(settings.config_file, 'r')))
    if not check_yaml(config):
        logger.error('Invalid yaml config file')
        os._exit(1)
except Exception as e:
    logger.error(e)
