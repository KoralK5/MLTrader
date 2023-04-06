import requests
from textblob import TextBlob
from bs4 import BeautifulSoup

stock_symbol = input('Stock Symbol: ')
url = f'https://www.marketwatch.com/investing/stock/{stock_symbol}/news'

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

        print(f'Title: {title}')
        print(f'Sentiment: {sentiment}')
        print()

print()
print(f'Stock: {stock_symbol}')
print(f'Total Score: {round(score, 1)} (x>5 => Buy)')
