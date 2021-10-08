from tkinter import *
import tweepy
import pandas as pd
from textblob import TextBlob
from matplotlib import pyplot as plt
import re

#导入窗口类
root = Tk()
root.title('Twitter Sentimental Analysis by Flora')

#设置查询框大小
root.geometry('550x400')

#将标题放置进小窗口中
#banner设置的是上下边框长度 padx pady分别为水平和垂直边框的长度
banner = Frame(root, padx=15, pady=14)
banner.pack()
heding = Label(banner,text="Twitter Sentimental Analysis", font="Arial 20")
heding.pack()

input_frame = Frame(root, padx=0, pady=30)
input_frame.pack()

#查询按钮
input_frame1 = Frame(root, padx=0, pady=0)
input_frame1.pack()

#分别为用户输入的Twi账号和话题名称
user_value = StringVar()
hash_value = StringVar()

#第一行 推特账号 使用grid放置部件
username = Label(input_frame, text=" Enter UserID (insert @+character) :)",font="Arial 10 bold", padx=30)
username.grid(row=2, column=1)
userinput = Entry(input_frame, textvariable=user_value)
userinput.grid(row=2, column=2)

#中间小间隔 or
blank2 = Label(input_frame, text="or")
blank2.grid(row=3, column=2)

#第二行 话题名称
hashtag = Label(input_frame, text=" Enter topics (insert #+character) :)", font="Arial 10 bold", padx=30)
hashtag.grid(row=4, column=1)
hashinput = Entry(input_frame, textvariable=hash_value)
hashinput.grid(row=4, column=2)

#错误显示
f1 = Frame(root, padx=15, pady=14)
f1.pack()

#错误1：都为空 错误2：都无效
error1 = Label(f1, text=" Fill at least one option :(", fg="red")
error2 = Label(f1, text=" Both entries are not valid :(", fg="red")

#查询之后的结果显示
f2 = Frame(root, padx=15, pady=14)
f2.pack()
po = Label(f2, text="Positive:", padx=20)
na = Label(f2, text="Negative:", pady=5, padx=20)
nt = Label(f2, text="Nertual:", padx=20)


#定义函数进行查询
def click():
    user_name = user_value.get()
    hash_name = hash_value.get()

    global number;

    # Twi API
    consumerKey = "Lr9BYDvg5Ed4qPnAvbgH5qM3x"
    consumerSecret = "M9zTp4mt52eknUJctlyZ7S6zefXbt93WV2Ox0ypfcTZn3FBtNK"
    accessToken = "1437467670618669058-Xc9586GVlPnkPCgRwo5wu76Yz08EIT"
    accessTokenSecret = "KulxyCEFXmXUO9KWTZaj7gB4bhyEVYMjYQkIF2I9ZLc6p"

    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
    authenticate.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    #第一种，直接报错
    if user_name == "" and hash_name == "":
        error1.grid()

    #第二种：有username
    elif hash_name == "":

        error1.grid_remove()
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

        po = Label(f2, text=f"Positive: {positive_per}%", padx=15).grid(row=1, column=2)
        na = Label(f2, text=f"Negative: {negative_per}%", pady=5, padx=15).grid(row=2, column=2)
        nt = Label(f2, text=f"Neutral: {neutral_per}%", padx=15).grid(row=3, column=2)
        su = Label(f2, text=f"Subjective: {subjective_per}%", padx=15).grid(row=4, column=2)
        ob = Label(f2, text=f"Objective: {objective_per}%", pady=5, padx=15).grid(row=5, column=2)


        labels = 'Positive', 'Negative', 'Neutral','Subjective', 'Objective'
        sizes = [positive_per, negative_per, neutral_per,subjective_per, objective_per]
        explode = (0, 0.1, 0,0,0.1)


        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
        number += 1

    elif user_name == "":
        error1.grid_remove()

        msgs = []
        msg = []
        #使用tweepy.cursor进行hashtay的搜索

        for tweet in tweepy.Cursor(api.search, q=hash_name).items(500):
            #加入元组，不可修改
            msg = [tweet.text]
            msg = tuple(msg)
            msgs.append(msg)

        def cleanTxt(text):
            #对于text做处理 去除以@ # https开头的单词，即用户名、超链接和话题
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

        po = Label(f2, text=f"Positive: {positive_per}%", padx=15).grid(row=1, column=2)
        na = Label(f2, text=f"Negative: {negative_per}%", pady=5, padx=15).grid(row=2, column=2)
        nt = Label(f2, text=f"Neutral: {neutral_per}%", padx=15).grid(row=3, column=2)
        su = Label(f2, text=f"Subjective: {subjective_per}%", padx=15).grid(row=4, column=2)
        ob = Label(f2, text=f"Objective: {objective_per}%", pady=5, padx=15).grid(row=5, column=2)


        labels = 'Positive', 'Negative', 'Neutral','Objective','Subjective'
        sizes = [positive_per, negative_per, neutral_per,objective_per,subjective_per]
        explode = (0.1, 0.1, 0.1,0,0)


        fig1, ax1 = plt.subplots()
        # 小数点前后各一位数 离中心距离的设置 label上加入百分比介绍的值 从y轴正方向画起
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')

        plt.show()

        number += 1
    else:
        error2.grid()


number = 0

button = Button(input_frame1, text="Analyze", command=click, fg="blue", height=1, width=15)
button.grid(row=1, column=1)
root.mainloop()