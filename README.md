# stockwise-news-api

**🐙 [RapidAPI](https://rapidapi.com/prostockwise/api/stockwise-news-forecast) | 💹 [Stockwise](https://stockwise.pro)**

## Introduction

Stockwise News Forecast API uses advanced artificial intelligence techniques to analyze news articles. Simply provide the URL, and our cutting-edge analysis pipeline will fetch the content and deliver a detailed forecast:

1. Concise summary of the news content
2. Forecasts of related stocks with reasoning

## Comparison with Traditional News Sentiment Analysis

Stockwise News Forecast API offers next-generation automated news sentiment analysis, significantly outperforming traditional methods.

| Feature | Stockwise News Forecast API | Traditional News Sentiment Analysis |
| --- | --- | --- |
| Input Type | Any news article via URL | Clean text only |
| Related Stocks or ETFs | Discovers relevant symbols using AI; can identify patient investment opportunities | Only stocks mentioned or manually listed |
| Output Type | Provides reasoning with sentiment; helps investors learn and make clearer decisions | Only simple positive or negative sentiment |

## Endpoints

1. **`POST /news_forecast`**
    
    **Request:**
    
    - `url` : url of original news
    
    ```json
    {
    	"url": "https://finance.yahoo.com/news/cut-or-pause-2-critical-reports-will-determine-what-fed-does-in-november-090014786.html"
    }
    ```
    
    **Response:**
    
    - `url` : url of original news
    - `title` : title of the news article
    - `description` : brief description or summary of the news article
    - `published_time`: publication time of the news article (may be `null`)
    - `has_article` : boolean indicating if the article content was successfully retrieved
    - `summary` : concise summary of the news content
    - `forecasts` : array of stock forecasts based on the news analysis, each forecast contains:
        - `analyze`: Reasoning behind the forecast
        - `symbol`: Stock symbol or ETF symbol
        - `direction`: Predicted price movement (positive, negative, or neutral)
    
    ```json
    {
      "url": "https://finance.yahoo.com/news/cut-or-pause-2-critical-reports-will-determine-what-fed-does-in-november-090014786.html",
      "title": "Cut or pause? 2 critical reports will determine what Fed does in November.",
      "description": "Two reports this week on inflation and the labor market could swing the final calculus for Fed policymakers as they weigh another rate cut at their Nov. 6-7 meeting.",
      "published_time": "2024-10-28T09:00:14.000Z",
      "has_article": true,
      "summary": "The Federal Reserve is deciding whether to cut interest rates or pause its current approach at the upcoming meeting on November 6-7. The decision depends heavily on two critical reports—one on inflation and another on the labor market. If inflation remains strong or the jobs market shows unexpectedly high job growth, it might sway the Fed to consider a pause. However, many analysts believe a cut of 25 basis points is likely to occur despite the reports. Traders see about a 90% chance of such a cut occurring, especially given the recent trends in core inflation and employment data.",
      "forecasts": [
        {
          "analyze": "Given the Fed is likely to proceed with its rate-cutting plan regardless of potential economic resilience indicated by upcoming reports, interest rate-sensitive sectors and stocks may benefit from the anticipated rate cut.",
          "symbol": "XLF",
          "direction": "positive"
        }
      ]
    }
    ```
    

## FAQ

### Why Use Stockwise News Forecast API?

Stockwise News Forecast API offers several key advantages for investors and financial analysts:

1. Real-time insights: The API provides up-to-the-minute analysis of news articles and their potential impact on stock prices, allowing users to stay ahead of market trends.
2. AI-powered accuracy: By utilizing advanced machine learning algorithms, the API delivers highly accurate predictions, reducing the margin of error in forecasting.

### Can Stockwise News Forecast API process any url?

It can process any URL that allows content fetching. However, if the real content is behind a login or paywall, it can't fetch and analyze it.

### Can Stockwise News Forecast API Make Mistakes?

Yes, mistakes can occur. While the Stockwise News Forecast API uses advanced artificial intelligence to provide accurate predictions, it's important to remember that no forecasting tool is 100% reliable. Markets are influenced by many complex factors, some of which may be unpredictable or not present in the news.

However, the API provides explanations to help users make more informed decisions. It details the reasoning behind each prediction, allowing users to understand the logic behind the forecast. This transparency enables investors to carefully evaluate the analysis results and incorporate them into a broader decision-making process.

The API is also continuously updated and improved to enhance long-term accuracy.