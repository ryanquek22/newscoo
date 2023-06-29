from pygooglenews import GoogleNews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import math

gn = GoogleNews()

search = gn.search('Microsoft', when = '6m')
titles = []
for item in search['entries']:
    titles.append(item.title)

df = pd.DataFrame({'MSFT' : titles})

analyzer = SentimentIntensityAnalyzer()

negative = []
neutral = []
positive = []
overall = [] #-1 is negative, 0 is neutral, 1 is positive

for i in range(len(titles)):
    temp_title = titles[i]
    title_analyzed = analyzer.polarity_scores(temp_title)
    #negative.append(title_analyzed['neg'])
    #neutral.append(title_analyzed['neu'])
    #positive.append(title_analyzed['pos'])
    
    if (max(title_analyzed['neg'], title_analyzed['neu'], title_analyzed['pos']) == title_analyzed['neg']):
        overall.append(-1)
    elif(max(title_analyzed['neg'], title_analyzed['neu'], title_analyzed['pos']) == title_analyzed['neu']):
        overall.append(0)
    else:
        overall.append(1)

df['overall'] = overall

df.to_csv('test.csv')

#print("\n")
#print(df)


