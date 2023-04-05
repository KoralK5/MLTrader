from newsapi import NewsApiClient
import datetime

newsapi = NewsApiClient(api_key='xd')

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
day = yesterday.strftime('%Y-%m-%d')

data = newsapi.get_everything(q='AAPL', from_param=day, sort_by='popularity')

amount = data['totalResults']
articles = data['articles']

print('Total Results:', amount)

for article in articles:
    print(article['title'])
    print(article['description'])
    print(article['url'])

print(data)
