from tkinter import *
import tweepy
import pandas as pd
from textblob import TextBlob
from matplotlib import pyplot as plt
import re

consumerKey = "Lr9BYDvg5Ed4qPnAvbgH5qM3x"
consumerSecret = "M9zTp4mt52eknUJctlyZ7S6zefXbt93WV2Ox0ypfcTZn3FBtNK"
accessToken = "1437467670618669058-Xc9586GVlPnkPCgRwo5wu76Yz08EIT"
accessTokenSecret = "KulxyCEFXmXUO9KWTZaj7gB4bhyEVYMjYQkIF2I9ZLc6p"

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

def judgeUser(user_name):
    global number;

    # Twi API
    #第二种：有username
    #获取近500条推特的信息并用pd进行造表
    post = api.user_timeline(screen_name=user_name, count=500, lang="en", tweet_mode="extended")
    twitter = pd.DataFrame([tweet.full_text for tweet in post], columns=['Tweets'])

    def cleanTxt(text):
            #将特殊符号全部替换为空格
        text = re.sub('@[A-Za-z0–9]+', '', text)  #  "@"
        text = re.sub('#', '', text)  # Hash tag '#'
        text = re.sub('https?:\/\/\S+', '', text)  # hyperlink
        return text

    twitter['Tweets'] = twitter['Tweets'].apply(cleanTxt)

        # polarity表示消极正向，subjectivity表示主观客观
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    twitter['Subjectivity'] = twitter['Tweets'].apply(getSubjectivity)
    twitter['Polarity'] = twitter['Tweets'].apply(getPolarity)

    def getAnalysis1(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    def getAnalysis2(score):
        if score < 0.5:
            return 'Subjective'
        else:
            return 'Objective'


    twitter['Analysis'] = twitter['Polarity'].apply(getAnalysis1)
    positive = twitter.loc[twitter['Analysis'].str.contains('Positive')]
    negative = twitter.loc[twitter['Analysis'].str.contains('Negative')]
    neutral1 = twitter.loc[twitter['Analysis'].str.contains('Neutral')]

    twitter['Analysis'] = twitter['Subjectivity'].apply(getAnalysis2)
    subjective = twitter.loc[twitter['Analysis'].str.contains('Subjective')]
    objective = twitter.loc[twitter['Analysis'].str.contains('Objective')]

    positive_per = round((positive.shape[0] / twitter.shape[0]) * 100, 1)
    negative_per = round((negative.shape[0] / twitter.shape[0]) * 100, 1)
    neutral_per = round((neutral1.shape[0] / twitter.shape[0]) * 100, 1)

    subjective_per = round((subjective.shape[0] / twitter.shape[0]) * 100, 1)
    objective_per = round((objective.shape[0] / twitter.shape[0]) * 100, 1)

    return positive_per,negative_per,neutral_per,subjective_per,objective_per

def judgeTopic(hash_name):
    global number;

    msgs = []
    # 使用tweepy.cursor进行hashtay的搜索

    for tweet in tweepy.Cursor(api.search, q=hash_name).items(500):
        # 加入元组，不可修改
        msg = [tweet.text]
        msg = tuple(msg)
        msgs.append(msg)

    def cleanTxt(text):
        # 对于text做处理 去除以@ # https开头的单词，即用户名、超链接和话题
        text = re.sub('@[A-Za-z0–9]+', '', text)
        text = re.sub('#', '', text)
        text = re.sub('https?:\/\/\S+', '', text)
        return text

    df = pd.DataFrame(msgs)
    df['Tweets'] = df[0].apply(cleanTxt)
    df.drop(0, axis=1, inplace=True)

    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)

    def getAnalysis1(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    def getAnalysis2(score):
        if score < 0.5:
            return 'Subjective'
        else:
            return 'Objective'

    df['Analysis'] = df['Polarity'].apply(getAnalysis1)
    positive = df.loc[df['Analysis'].str.contains('Positive')]
    negative = df.loc[df['Analysis'].str.contains('Negative')]
    neutral = df.loc[df['Analysis'].str.contains('Neutral')]

    df['Analysis'] = df['Subjectivity'].apply(getAnalysis2)
    subjective = df.loc[df['Analysis'].str.contains('Subjective')]
    objective = df.loc[df['Analysis'].str.contains('Objective')]

    positive_per = round((positive.shape[0] / df.shape[0]) * 100, 1)
    negative_per = round((negative.shape[0] / df.shape[0]) * 100, 1)
    neutral_per = round((neutral.shape[0] / df.shape[0]) * 100, 1)

    objective_per = round((objective.shape[0] / df.shape[0]) * 100, 1)
    subjective_per = round((subjective.shape[0] / df.shape[0]) * 100, 1)

    return positive_per,negative_per,neutral_per,subjective_per,objective_per

def report_wrong():
    return ("Useless input")

if __name__ == '__main__':
    input_example = input("Please type in an username or a topic")
    if input_example.startswith('@'):
        user_name = input_example
        print(judgeUser(user_name))
    elif input_example.startswith('#'):
        hash_name = input_example
        print(judgeTopic(hash_name))
    else:
        error_return=report_wrong()
        print(error_return)
