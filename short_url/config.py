from __future__ import annotations

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    NODE_ID: int
    PORT: int
    DB_NAME: str
    SHORT_URL_TEMPLATE: str


config = Config()
