from typing import Optional

from loguru import logger
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    jina_api_key: str
    # set url if use third-party openai service
    openai_url: Optional[str] = None
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    # if enabled, use polygon to fetch all symbols
    enable_symbol_filter: bool = False
    polygon_api_key: Optional[str] = None


config = Config()
logger.info(f"config: {config}")
