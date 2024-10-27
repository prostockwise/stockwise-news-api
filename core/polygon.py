from datetime import datetime, timedelta, date

import pytz
import requests
from pydantic import BaseModel
from tenacity import retry

from .config import config


def get_new_york_yesterday() -> date:
    # get timezone in NewYork
    new_york_tz = pytz.timezone("America/New_York")

    # get current datetime in NewYork
    ny_time = datetime.now(new_york_tz)

    # get yesterday
    return ny_time.date() - timedelta(days=1)


class DailyBar(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int


@retry
def get_grouped_daily_bars(_date: date) -> list[DailyBar]:
    """
    https://polygon.io/docs/stocks/get_v2_aggs_grouped_locale_us_market_stocks__date

    :param _date: yyyy-mm-dd
    :return:
    """
    url = (
            "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/"
            + _date.strftime("%Y-%m-%d")
    )
    r = requests.get(
        url,
        params={"adjusted": "false", "include_otc": "false", "apiKey": config.polygon_api_key},
    )
    r.raise_for_status()
    body = r.json()
    if body.get("status") != "OK":
        raise Exception(f"status is not OK: {body.get('status')}")
    results = []
    # if not trading day, no data found
    results_count = body.get("resultsCount", 0)
    if results_count > 0:
        for r in body["results"]:
            results.append(
                DailyBar(
                    symbol=r["T"],
                    open=r["o"],
                    high=r["h"],
                    low=r["l"],
                    close=r["c"],
                    volume=r["v"],
                )
            )
    return results


def fetch_latest_grouped_daily_bars() -> list[DailyBar]:
    date_ = get_new_york_yesterday()
    while True:
        daily_bars = get_grouped_daily_bars(date_)
        if len(daily_bars) > 0:
            return daily_bars
        # move date_ one day before
        date_ = date_ - timedelta(days=1)
