# -*- coding: utf-8 -*-
"""Data Process with Text Processing

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TkRPX3NZIX1dnvQQWMJVT-PlZyCf41UC
"""

import pandas as pd

medium_data = pd.read_csv('medium_data.csv',parse_dates= ['date'],dayfirst=True)

no_id = medium_data
df = no_id[['date','publication','title','subtitle','reading_time','responses','claps','url']].copy()
df.head(2)

"""Clearing Data Proses"""

#Data Cleaning (Fill NaN)
df['subtitle'].fillna('blank subtitles',inplace = True)
df['claps'].fillna(0,inplace = True)

#Output Test
# df

#setting data type in DataFrame
df['title'] = df['title'].astype('string')
df['subtitle'] = df['subtitle'].astype('string')
df['claps'] = df['claps'].astype('int')

#check NaN or nul in dataFrame
df['claps'].isnull().value_counts()

#Check Duplicate
check_duplicate = df[df.duplicated()]

#Remove Duplicate
df.drop_duplicates(subset =['date','publication','title','subtitle','reading_time','responses','claps','url'], inplace = True)

#Output Test
# df

import re

#Data Cleaning (clear symbol and other)
collect_title = []
collect_subtitle = []

for i in df['title']:
  new_title = re.sub(r"<(.*?)>","",i)
  collect_title.append(new_title)

for j in df['subtitle']:
  new_subtitle = re.sub(r"<(.*?)>","",j)
  collect_subtitle.append(new_subtitle)

df['title'] = collect_title
df['subtitle'] = collect_subtitle

#output test
# df

#save file
save  = df
save.to_csv('medium_data_clear.csv')

"""Text Processing with NLTK"""

import nltk 
nltk.download('all')

#collect title
medium_data = df[['date','publication','title','subtitle','reading_time','responses','claps']]

all_title ='*'
for i in medium_data['title']:
  all_title += i + ' '

#output
print(all_title)

#case folding
import re
import string

sub_sentence = re.sub(r"<(.*?)>"," ",all_title) #menghilangkan karakter yang berawalan < dan berakhiran > 
lower_title=sub_sentence.lower() #membuat lower
remove_punctuationmark = lower_title.translate(str.maketrans("","",string.punctuation)) #menghilangkan tanda baca selian "-
sub_number = re.sub(r"\d+","",lower_title) #menghilangkan angka
sub_notword = re.sub(r"\W"," ",sub_number) #menghilangkan karakter lain selian huruf
sub_doublespace = re.sub(r"\s+"," ",sub_notword ) #menghilangkan spasi double

#Output
print(sub_doublespace)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Tokenizing 
tokens = nltk.word_tokenize(sub_doublespace)

#Filtering (Stopword Removal)
liststopwords = stopwords.words('english')

word_filter = []
for w in tokens:
  if w not in liststopwords:
    word_filter.append(w)

#output
print(tokens)
print(word_filter)

from nltk.stem import WordNetLemmatizer

#Steming Process
wnl = WordNetLemmatizer()

after_steming = []
for k in word_filter:
  after_steming.append(wnl.lemmatize(k))

#output
print(after_steming)
# for k in word_filter:
#   print(k, " : ", wnl.lemmatize(k))

from nltk.probability import FreqDist
import matplotlib.pyplot as plt

#collect list count
word_freq = nltk.FreqDist(after_steming)

#output
print(word_freq.most_common())
plt.figure(figsize=(14,5))
word_freq.plot(70,cumulative=False)

import pandas as pd
import matplotlib.pyplot as plt

#convert frequence to Dataframe
freg_word = pd.DataFrame.from_dict(word_freq,orient='index')
freg_word.columns = ['Title']
freg_word.index.name = 'Kata'

freg_word = freg_word.sort_values(by =['Title'], ascending=False)

#visualization & Output
ax = freg_word.head(10).plot.bar()
ax.bar_label(ax.containers[0]) #anotate bar
plt.title('''
  Tren Kata Kunci dalam Judul Artikel 
  di Platform Medium Bulan Januari-Maret 2023
  ''')
plt.ylabel('Frekuensi')