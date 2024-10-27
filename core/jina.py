from typing import Optional

import requests
from pydantic import BaseModel
from tenacity import retry

from .config import config


class JinaContent(BaseModel):
    title: str
    description: str
    url: str
    content: str
    publishedTime: Optional[str]


@retry
def jina_reader(url: str) -> JinaContent:
    """
    fetch page to markdown by jina reader api, response sample:
    {
      "code": 200,
      "status": 20000,
      "data": {
        "title": "Example Domain",
        "description": "",
        "url": "https://example.com/",
        "content": "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.\n\n[More information...](https://www.iana.org/domains/example)",
        "publishedTime": "2024-10-10T11:02:52.000Z",
        "usage": {
          "tokens": 42
        }
      }
    }

    :param url: web page to fetch
    :return: data in jina response
    """
    r = requests.get(
        "https://r.jina.ai/" + url,
        headers={
            "Authorization": "Bearer " + config.jina_api_key,
            "X-Locale": "en-US",
            "Accept": "application/json",
        },
        timeout=10,
    )
    r.raise_for_status()
    content = r.json()
    if content.get("code") != 200:
        raise Exception("code != 200, url: " + url)
    content = content["data"]
    return JinaContent(
        title=content.get("title", ""),
        description=content.get("description", ""),
        url=content.get("url", ""),
        content=content.get("content", ""),
        publishedTime=content.get("publishedTime", None),
    )
