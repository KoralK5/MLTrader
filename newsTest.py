import requests
from textblob import TextBlob
from bs4 import BeautifulSoup

buyTresh = 4
sellTresh = 2

# Set the URL for the MarketWatch news page for a given stock
stock_symbol = input('Stock Symbol: ')
url = f'https://www.marketwatch.com/investing/stock/{stock_symbol}/news'

# Make a request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the news articles from the HTML content
articles = soup.find_all('div', {'class': 'article__content'})

# Print the titles and summaries of the news articles
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
print(f'Total Score: {score}')
print(f'Signals: x>{buyTresh} -> BUY | x<{sellTresh} -> SELL')

