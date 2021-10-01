from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import io
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\Flora\\Downloads\\my-project-ec601-327101-52b03cf281db.json'
# If you don't specify credentials when constructing the client, the
# client library will look for credentials in the environment.

def calc_sentiment_one_sentence():
    # Instantiates a client
    client = language.LanguageServiceClient()

    document = types.Document(
        content = 'I hate to do this over and over again',
        type=enums.Document.Type.PLAIN_TEXT,
    )
    # Call API to analyze text.
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print("Sentence text: " + document.content)
    print("Sentence sentiment score:" + str(sentiment.score))
    print(u"Sentence sentiment magnitude:" + str(sentiment.magnitude))
    print("---------------------------")


def calc_sentiment_poem():

    client = language.LanguageServiceClient()
    input_file = "load.txt"
    with io.open(input_file, "r") as inp:
        docu = inp.read()

    text = types.Document(content=docu,
                          type=enums.Document.Type.PLAIN_TEXT)

    annotation = client.analyze_sentiment(document=text)

    score = annotation.document_sentiment.score
    magnitude = annotation.document_sentiment.magnitude
    print("The sentiment analysis for the poem 《Death, Be Not Proud》by John Donne")

    for index, sentence in enumerate(annotation.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence #{} Sentiment score: {}'.format(
            index + 1, sentence_sentiment))

    print('Score: {}, Magnitude: {}'.format(score, magnitude))

calc_sentiment_one_sentence()

calc_sentiment_poem()

