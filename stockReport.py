import requests
import os
from textblob import TextBlob
from bs4 import BeautifulSoup

stockType = input('Stock Type: ')
stockFile = os.getcwd() + f'\\symbols\\{stockType}.txt'

f = open(stockFile, 'r').read().splitlines()
stockNames = [i[:i.index('\t')] for i in f][1:]

results = []
for stock_symbol in stockNames:
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

            '''
            print(f'Title: {title}')
            print(f'Sentiment: {sentiment}')
            print()
            '''

    results.append((score, stock_symbol))

    print(f'\nStock: {stock_symbol}')
    print(f'Total Score: {round(score, 1)}')

results = sorted(results, reverse=True)

print('\n')
print('RESULTS')
for i in results:
    print(f'{i[1]}: {round(i[0], 2)}')

