import requests
from textblob import TextBlob
from bs4 import BeautifulSoup

def sentiments(stockNames, progress=False):
    idx = 1
    n = len(stockNames)
    results = {}
    for stock_symbol in stockNames:
        if progress:
            print(f'Progress: {idx}/{n}', end='\r')
        url = f'https://www.marketwatch.com/investing/stock/{stock_symbol}'

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', {'class': 'article__content'})

        score = 0
        for article in articles:
            title = ' '.join(article.find('h3', {'class': 'article__headline'}).text.split())
            if len(title):
                blob = TextBlob(title)
                sentiment = blob.sentiment.polarity

                score += sentiment

        results[stock_symbol] = score
        idx += 1

    return results
