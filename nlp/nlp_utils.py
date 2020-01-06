#!/usr/bin/python

import re
from string import punctuation

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import nltk
nltk.download('wordnet')

# Config
max_features = 50  # max features to be used in TfidfVectorizer
stemming = True
lemmatization = True
lowercase = False
remove_stops = True
stops = ['the','a','an','and','but','if','or','because','as','what','which','this','that','these','those','then',
              'just','so','than','such','both','through','about','for','is','of','while','during','to','What','Which',
              'Is','If','While','This']
# punctuation = punctuation.replace('_','')

lemmatizer = WordNetLemmatizer()
tf = TfidfVectorizer(max_features=max_features, stop_words='english')
st = PorterStemmer()

def ExtractText(data):
    def Prune(s):
        if not s:
            return ''
        return s
    def StripFromEnd(s):
        return re.sub(r'\[.+\]$', '', Prune(s))
    def Special(pre, text):
        if not text or text == '':
            return ''
        return pre + '_' + Prune(text).replace(' ', '-')
    def ExtractItem(item):
        return ' '.join([Prune(item['title']),
                         Prune(item['description']),
                         StripFromEnd(item['content'])])
    def PostExtraction(txt):
        return ' '.join([txt, Special('author', item['author']),
                        Special('country', item['country']),
                        Special('category', item['category'])])
    def ApplyOpts(txt):
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
        # txt = re.sub(r"review", "", txt))
        # txt = re.sub(r"Review", "", txt)
        # txt = re.sub(r"TripAdvisor", "", txt))
        # txt = re.sub(r"reviews", "", txt)
        # txt = re.sub(r"Hotel", "", txt)
        # txt = re.sub(r"what's", "", txt)
        # txt = re.sub(r"What's", "", txt)
        # txt = re.sub(r"\'s", " ", txt)
        # txt = txt.replace("pic", "picture")
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
        txt = ''.join([c for c in txt if c not in punctuation])

        # Remove all symbols
        # txt = re.sub(r'[^A-Za-z0-9\s]',r' ',txt)
        txt = re.sub(r'\n',r' ',txt)

        if remove_stops:
            txt = ' '.join([w for w in txt.split() if w not in stops])
        if lowercase:
            txt = ' '.join([w.lower() for w in txt.split()])
        if stemming:
            txt = ' '.join([st.stem(w) for w in txt.split()])
        if lemmatization:
            txt = ' '.join([lemmatizer.lemmatize(w, pos='v') for w in txt.split()])
        return txt

    result = [''] * len(data)
    for i, item in enumerate(data):
        result[i] = ApplyOpts(ExtractItem(item))
        result[i] = PostExtraction(result[i])
    return result

def TfIdfScores(news, liked = []):
    extracted_news = ExtractText(news)
    print('extracted_news[1]', extracted_news[1])
    fit_transform = tf.fit_transform(extracted_news)
    print('tf.get_feature_names()', tf.get_feature_names())
    for i,_ in enumerate(news):
        news[i]['v'] = fit_transform[i].todense().tolist()[0]

    if len(liked) > 0:
        extracted_liked = ExtractText(liked)

        transform = tf.transform(extracted_liked)
        for i,_ in enumerate(liked):
            liked[i]['v'] = transform[i].todense().tolist()[0]

    return news, liked

