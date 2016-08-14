import facebook
import dateutil.parser as dateparser
from nltk.sentiment.vader import SentimentIntensityAnalyzer


token = ''
graph = facebook.GraphAPI(access_token=token, version='2.7')


# filter=stream&comments?fields=parent,message,from,likes,created_time'
def get_comments(id_post):
    comments = graph.get_connections(id=id_post, connection_name='comments?filter=stream&fields=parent,message,from,likes,created_time', limit=610)
    return comments


def get_object_by_id(id):
    object = graph.get_object(id)
    return object


# Function get all coments from id-post
def get_comments_format(id_post):
    sentences_comments = []
    time_comments = []
    comments = graph.get_connections(id=id_post, connection_name='comments', limit = 1000)
    cnt = 0
    for comment in comments['data']:
        try:
            cnt = cnt + 1
            print('Comment {0} : {1} -- Time = {2}'.format(cnt, comment['message'], comment['created_time']))
            sentences_comments.append(comment['message'])
            time_comments.append(comment['created_time'])
        except:
            continue
    return sentences_comments, time_comments


# Convert time comment to coordinate X in Graph
def time_to_x(time_comments, created_time_post):
    timeX = []
    for time_comment in time_comments:
        distTime = dateparser.parse(time_comment) - created_time_post
        x = int(distTime.total_seconds())
        timeX.append(x)
    return timeX


#  Sentiment Analysis comment using NLTK library
def sentiment_analysis(sentences_comments):
    allY = []
    posY = []
    negY = []
    sid = SentimentIntensityAnalyzer()
    sumPos = 0
    sumNeg = 0
    sumAll = 0
    cnt = 0
    for sentence in sentences_comments:
        cnt += 1
        ss = sid.polarity_scores(sentence)
        for type in sorted(ss):
            if type == "neg":
                sumNeg += ss[type]
                negY.append(sumNeg / cnt)
            if type == "pos":
                sumPos += ss[type]
                posY.append(sumPos / cnt)
            if type == 'compound':
                sumAll += ss[type]
                allY.append(sumAll / cnt)
    return posY, negY, allY

