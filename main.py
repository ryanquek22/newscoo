from pygooglenews import GoogleNews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import math
import logging
import logging.handlers
import os
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024*1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available"
    


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

average_score = np.mean(df['overall'])
#df.to_csv('test.csv')

logger.info(f"Token value: {SOME_SECRET}")
logger.info(f"Average Vader Sentiment of 100 Mircrosoft articles over the past 6 months is {average_score} ")


