import enum
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel
from tenacity import retry

from .config import config

openai = OpenAI(
    base_url=config.openai_url,
    api_key=config.openai_api_key,
)


class Direction(str, enum.Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


class Forecast(BaseModel):
    analyze: str
    symbol: str
    direction: Direction

    class Config:
        use_enum_values = True


class NewsForecasts(BaseModel):
    has_article: bool
    summary: str
    forecasts: list[Forecast]


@retry
def news_forecasts(content: str, symbols: Optional[set[str]]) -> NewsForecasts:
    """
    :param content: webpage extract by jina reader API.
    :param symbols: filter by symbols list
    :return: structured analyze by AI
    """
    completion = openai.beta.chat.completions.parse(
        model=config.openai_model,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI assistant specialized in analyzing news and give insights of investing, Your processing pipeline is:
1. Read markdown text extracted from websites and check whether has article.
2. If has_article, then summary the article in plain English for investors.
3. If has_article, then analysing potential investment opportunities, tell the symbol(Stock or ETF) and predict the direction(positive or negative).
4. You should give the reasonable forecasts. Don't make forecasts based on fantasy.
5. Symbol MUST be TradingView supported Stock or ETF.
""".strip(),
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        response_format=NewsForecasts,
    )
    analyze: NewsForecasts = completion.choices[0].message.parsed
    if symbols:  # filter by symbols
        forecasts = [f for f in analyze.forecasts if f.symbol in symbols]
        analyze.forecasts = forecasts
    return analyze
