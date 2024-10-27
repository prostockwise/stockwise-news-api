import time
from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from core.ai import Forecast, news_forecasts
from core.config import config
from core.jina import jina_reader
from core.polygon import fetch_latest_grouped_daily_bars

app = FastAPI()


class NewsForecastRequest(BaseModel):
    url: str


class NewsForecastResponse(BaseModel):
    url: str
    title: str
    description: str
    published_time: Optional[str]
    has_article: bool
    summary: str
    forecasts: list[Forecast]


_symbols: set
_symbols_updated_at: datetime


def update_symbols():
    global _symbols
    global _symbols_updated_at
    start_time = time.time()
    daily_bars = fetch_latest_grouped_daily_bars()
    logger.info(f"Fetch symbols in {time.time() - start_time}s")
    _symbols = set([d.symbol for d in daily_bars])
    _symbols_updated_at = datetime.now()


@app.post("/news_forecast")
def news_forecast(req: NewsForecastRequest) -> NewsForecastResponse:
    start_time = time.time()
    content = jina_reader(req.url)
    logger.info(f"Fetch news: {req.url} in {time.time() - start_time}s")
    if config.enable_symbol_filter:
        # update symbols every day
        if _symbols_updated_at < datetime.now() - timedelta(days=1):
            update_symbols()
    start_time = time.time()
    forecasts = news_forecasts(
        content.content, _symbols if config.enable_symbol_filter else None
    )
    logger.info(f"Forecast news: {req.url} in {time.time() - start_time}s")
    return NewsForecastResponse(
        url=req.url,
        title=content.title,
        description=content.description,
        published_time=content.publishedTime,
        has_article=forecasts.has_article,
        summary=forecasts.summary,
        forecasts=forecasts.forecasts,
    )


if __name__ == "__main__":
    if config.enable_symbol_filter:
        update_symbols()
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
