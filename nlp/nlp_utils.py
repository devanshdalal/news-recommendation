#!/usr/bin/python

import re
from string import punctuation

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import nltk
import urllib.parse

# Config
max_features = 100  # max features to be used in TfidfVectorizer
stemming = False
lemmatization = False
lowercase = True
remove_stops = True
stops = set.union(
    set(map(lambda x: x.strip(),
            open('nlp/stops.txt').readlines())),
    set(map(lambda x: x.strip(),
            open('nlp/10000.txt').readlines())))
# punctuation = punctuation.replace('_','')

lemmatizer = None
if lemmatization:
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
tf = TfidfVectorizer(max_features=max_features, stop_words=stops)
st = None
if stemming:
    st = PorterStemmer()


def ExtractText(data):
    def Prune(item, s):
        if s not in item or not item[s] or item[s] == None:
            return ''
        return item[s]

    def StripFromEnd(item, s):
        return re.sub(r'\[.+\]$', '', Prune(item, s))

    def AddAuthorInfo(item):
        id = 'author'
        if id not in item or item[id] == None or item[id] == '':
            return ''
        extracted_author = None 
        if 'http' in item[id]:
            extracted_author = urllib.parse.urlparse(item[id]).netloc
            extracted_author = extracted_author.replace('.', '')
        else:
            extracted_author = item[id].replace(' ', '-')
        return id + '_' + extracted_author

    def ExtractItem(item):
        return ' '.join([
            Prune(item, 'title'),
            Prune(item, 'description'),
            StripFromEnd(item, 'content')
        ])

    def PostExtraction(item, txt):
        return ' '.join([txt, AddAuthorInfo(item)])

    def ApplyOpts(txt):
        if lowercase:
            txt = ' '.join([w.lower() for w in txt.split()])
        # Replace apostrophes with standard lexicons
        txt = txt.replace("isn't", "is not")
        txt = txt.replace("aren't", "are not")
        txt = txt.replace("ain't", "am not")
        txt = txt.replace("won't", "will not")
        txt = txt.replace("didn't", "did not")
        txt = txt.replace("shan't", "shall not")
        txt = txt.replace("haven't", "have not")
        txt = txt.replace("hadn't", "had not")
        txt = txt.replace("hasn't", "has not")
        txt = txt.replace("don't", "do not")
        txt = txt.replace("wasn't", "was not")
        txt = txt.replace("weren't", "were not")
        txt = txt.replace("doesn't", "does not")
        txt = txt.replace("'s", " is")
        txt = txt.replace("'re", " are")
        txt = txt.replace("'m", " am")
        txt = txt.replace("'d", " would")
        txt = txt.replace("'ll", " will")

        # More cleaning
        txt = re.sub(r"can't", "cannot ", txt)
        txt = re.sub(r"\'ve", " have ", txt)
        txt = re.sub(r"n't", " not ", txt)
        txt = re.sub(r"I'm", "I am", txt)
        txt = re.sub(r" m ", " am ", txt)
        txt = re.sub(r"\'re", " are ", txt)
        txt = re.sub(r"\'d", " would ", txt)
        txt = re.sub(r"\'ll", " will ", txt)
        # txt = re.sub(r"60k", " 60000 ", txt)
        txt = re.sub(r" e g ", " eg ", txt)
        txt = re.sub(r" b g ", " bg ", txt)
        # txt = re.sub(r"\0s", "0", txt)
        txt = re.sub(r" 9 11 ", "911", txt)
        txt = re.sub(r"e-mail", "email", txt)
        # txt = re.sub(r"\s{2,}", " ", txt)
        # txt = re.sub(r"quikly", "quickly", txt)
        txt = re.sub(r" usa ", " America ", txt)
        txt = re.sub(r" USA ", " America ", txt)
        txt = re.sub(r" u s ", " America ", txt)
        txt = re.sub(r" uk ", " England ", txt)
        txt = re.sub(r" UK ", " England ", txt)
        txt = re.sub(r"india", "India", txt)
        txt = re.sub(r"switzerland", "Switzerland", txt)
        txt = re.sub(r"china", "China", txt)
        txt = re.sub(r"chinese", "Chinese", txt)
        txt = re.sub(r"imrovement", "improvement", txt)
        txt = re.sub(r"intially", "initially", txt)
        txt = re.sub(r"quora", "Quora", txt)
        txt = re.sub(r" dms ", "direct messages ", txt)
        txt = re.sub(r"demonitization", "demonetization", txt)
        # txt = re.sub(r"actived", "active", txt)
        txt = re.sub(r"kms", " kilometers ", txt)
        txt = re.sub(r"KMs", " kilometers ", txt)
        txt = re.sub(r" cs ", " computer science ", txt)
        txt = re.sub(r" upvotes ", " up votes ", txt)
        txt = re.sub(r" iPhone ", " phone ", txt)
        txt = re.sub(r"\0rs ", " rs ", txt)
        txt = re.sub(r"calender", "calendar", txt)
        txt = re.sub(r"ios", "operating system", txt)
        txt = re.sub(r"gps", "GPS", txt)
        txt = re.sub(r"gst", "GST", txt)
        txt = re.sub(r"programing", "programming", txt)
        txt = re.sub(r"bestfriend", "best friend", txt)
        txt = re.sub(r"dna", "DNA", txt)
        txt = re.sub(r"III", "3", txt)
        txt = re.sub(r"the US", "America", txt)
        txt = re.sub(r"Astrology", "astrology", txt)
        txt = re.sub(r"Method", "method", txt)
        txt = re.sub(r"Find", "find", txt)
        txt = re.sub(r"banglore", "Banglore", txt)
        txt = re.sub(r"congress", "Congress", txt)
        txt = re.sub(r"bjp", "BJP", txt)
        txt = re.sub(r" J K ", " JK ", txt)

        # Remove urls and emails
        txt = re.sub(r'^https?:\/\/.*[\r\n]*', ' ', txt, flags=re.MULTILINE)
        txt = re.sub(r'[\w\.-]+@[\w\.-]+', ' ', txt, flags=re.MULTILINE)

        # Remove punctuation from text
        txt = ''.join([c if c not in punctuation else ' ' for c in txt])

        # Remove all symbols
        # txt = re.sub(r'[^A-Za-z0-9\s]',r' ',txt)
        txt = re.sub(r'\n', r' ', txt)

        # Remove all number only words
        txt = re.sub(r'\b(\d+)\b', r'', txt)

        if remove_stops:
            txt = ' '.join([w for w in txt.split() if w not in stops])
        if stemming:
            txt = ' '.join([st.stem(w) for w in txt.split()])
        if lemmatization:
            txt = ' '.join(
                [lemmatizer.lemmatize(w, pos='v') for w in txt.split()])
        return txt

    result = [''] * len(data)
    for i, item in enumerate(data):
        result[i] = ApplyOpts(ExtractItem(item))
        # print('result[i]', ExtractItem(item))
        result[i] = PostExtraction(item, result[i])
    return result


def TfIdfScores(news, tfidfVectorizer):
    extracted_news = ExtractText(news)
    print('extracted_news[1]', extracted_news[1])
    fit_transform = tfidfVectorizer.fit_transform(extracted_news)
    print("tfidfVectorizer.vocabulary_", tfidfVectorizer.vocabulary_)
    weights = list(map(lambda x: {x[0]: x[1]}, zip(tfidfVectorizer.get_feature_names(), tfidfVectorizer.idf_)))
    print('weights', weights)
    for i, _ in enumerate(news):
        news[i]['v'] = fit_transform[i].todense().tolist()[0]


    return news, tfidfVectorizer

def AddTfIdfWeights(liked, tfidfVectorizer):
    extracted_liked = list(map(lambda x: x['article'], liked))
    extracted_liked = ExtractText(extracted_liked)

    print('extracted_liked', extracted_liked)
    transform = tfidfVectorizer.transform(extracted_liked)
    for i, _ in enumerate(liked):
        liked[i]['article']['v'] = transform[i].todense().tolist()[0]
    return liked
