import nltk
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import nltk
import re
import parsing
import os
import codecs
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from databaseConnection import Database
from operator import *
#from gensim import corpora, models, similarities
import unicodedata
import string


#from sklearn import feature_extraction
#import mpld3

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

def tokenize_and_stem(text):
    stemmer = SnowballStemmer('english')
    tokens= [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        token = remove_accents(token)
        if re.search('[a-zA-Z]', token):
            if(len(token)>1 and len(token)<100):
                filtered_tokens.append(token)
    stems=[]
    stems = [stemmer.stem(t) for t in  filtered_tokens]
    return stems

def tokenize_only(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []

    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def count_main_list(dataset):
    token_list = []
    count_list = []

    for set in dataset:
        for temp_tuple in set:
            token = temp_tuple[0]
            tf = temp_tuple[1]
            try:
                tokenIndex = token_list.index(token)
                count_list[tokenIndex][1]+= 1
                count_list[tokenIndex][2] += tf
            except ValueError:
                token_list.append(token)
                count_list.append([token, 1, tf])
    return count_list

def count_words(string_list):
    import string
    #string_list = s.split(" ")
    #string_list = sorted(s.split(" "), key=str)
    #print(string_list)
    #exit(0)
    wordList = []
    countList = []
    for word in string_list:
        #print(word + "| ")
        word = word.strip()
        try:
            wordIndex = wordList.index(word)
            countList[wordIndex][1]+= 1
        except ValueError:
            wordList.append(word)
            countList.append([word, 1])
    return countList

def normalizeString(content):
    content = content.replace("'", '')
    content = content.replace('"', '')
    content = content.replace('/', ' ')
    content = content.replace('\\', ' ')
    content = content.replace(',', ' ')
    content = content.replace('μ', 'µ')
    content = content.replace('ß', 'β')
    content = content.replace('(', ' ')
    content = content.replace(')', ' ')
    content = content.replace('%', ' ')
    content = content.replace(':', ' ')
    content = content.replace('.', ' ')
    content = content.replace('∙', ' ')
    content = content.replace('˚', '°')
    content = content.replace('~', ' ')
    content = content.replace('=', ' ')
    content = content.replace('≤', ' ')
    content = content.replace('−', '-')
    content = content.replace('α', 'a')
    content = content.replace('δ', 'b')
    return content


#get row data from database
data = Database()
stopwords = nltk.corpus.stopwords.words('english')
synopses = data.getAbstract()

#initial abstract list
abstract_list=[]
TotalCountList = []

for i in synopses:
    abstract_id = i[0]
    abstract_list.append(str(abstract_id))

    content = normalizeString(i[1])
    allwords_stemmed = tokenize_and_stem(content)
    allwords_stemmed = [word for word in allwords_stemmed if word not in stopwords]
    count_list = count_words(allwords_stemmed)
    #print(tuple_count)
    TotalCountList.append(count_list)

    #calculate result for every 100 abstracts and insert result to database.
    if (len(abstract_list) == 100):
        result = count_main_list(TotalCountList)
        TotalCountList = []
        #join abstract_ids to a comma breaken string
        abstract_str = ",".join(abstract_list)
        abstract_list = []

        token_list = []
        df_value_list = []
        tf_value_list = []
        for temp_tuple in result:
            token_list.append(temp_tuple[0].strip())
            df_value_list.append(str(temp_tuple[1]))
            tf_value_list.append(str(temp_tuple[2]))
        #join tf and df lists to comma breaked strings
        token_str = ",".join(token_list)
        df_str = ",".join(df_value_list)
        tf_str = ",".join(tf_value_list)

        print(abstract_str)
        print(token_str)
        print(df_str)
        print(tf_str)
        data.insertToken(abstract_str, token_str, df_str, tf_str)
        print("inserted %s tokens into database" % str(len(token_list)))

if(len(abstract_list) > 0 ):
    result = count_main_list(TotalCountList)
    TotalCountList = []
    # join abstract_ids to a comma breaken string
    abstract_str = ",".join(abstract_list)
    abstract_list = []

    token_list = []
    df_value_list = []
    tf_value_list = []
    for temp_tuple in result:
        token_list.append(temp_tuple[0].strip())
        df_value_list.append(str(temp_tuple[1]))
        tf_value_list.append(str(temp_tuple[2]))
    # join tf and df lists to comma breaked strings
    token_str = ",".join(token_list)
    df_str = ",".join(df_value_list)
    tf_str = ",".join(tf_value_list)

    print(abstract_str)
    print(token_str)
    print(df_str)
    print(tf_str)
    data.insertToken(abstract_str, token_str, df_str, tf_str)
    print("inserted %s tokens into database" % str(len(token_list)))
exit(0)

for i in range(1,len(synopses)):


    print('loading database')
    #synopses = data.table()

    print('finished Load database')

    TotalCountList = []
    abstract_list = []
    tuple_count = 0;
    for i in synopses:
        abstract_id = i[0]
        abstract_list.append(str(abstract_id))
        content = normalizeString(i[1])
        allwords_stemmed = tokenize_and_stem(content)
        allwords_stemmed = [word for word in allwords_stemmed if word not in stopwords]
        count_list = count_words(allwords_stemmed)
        tuple_count += len(count_list)
        ##print(tuple_count)
        TotalCountList.append(count_list)
    result = count_main_list(TotalCountList)
    token_list=[]
    df_value_list=[]
    tf_value_list=[]

    for temp_tuple in result:
        token_list.append(temp_tuple[0].strip())
        df_value_list.append(str(temp_tuple[1]))
        tf_value_list.append(str(temp_tuple[2]))
    #print(len(token_list))
    #token_list = np.unique(token_list)
    #for token in token_list:
        #print(token)
    #print(len(token_list))
    #exit(0);

    if False:
        token_list = np.unique(token_list)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print(token_list)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(df_value_list)

        print('_____________________')
        print(tf_value_list)
        # print(len(word_count))
        exit(0)

# allwords_stemmed = [word for word in allwords_stemmed if word not in totalvocab_stemmed]
    token_str = ", ".join(token_list)
    df_str = ", ".join(df_value_list)
    tf_str = ", ".join(tf_value_list)
    abstract_str = ", ".join(abstract_list)
    if False:
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print(token_str)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(df_str)
        token_list = np.unique(token_list)
        print('_____________________')
        print(tf_str)
        # print(len(word_count))
        #exit(0)
    data.insertToken(abstract_str, token_str, df_str, tf_str)
    print("inserted %s tokens into database" % str(len(token_list)))

exit(0)

#tokenize
#tokenized_text = [tokenize_and_stem(text) for text in synopses]

#remove stop words
#texts = [[word for word in text if word not in stopwords] for text in tokenized_text]
count=0
for i in synopses:

    abstract_id = i[0]
    count += 1
    content = normalizeString(i[1])
    allwords_stemmed = tokenize_and_stem(content)

    allwords_stemmed = [word for word in allwords_stemmed if word not in stopwords]
    #allwords_stemmed = np.unique(allwords_stemmed)
    count_list = count_words(allwords_stemmed)

    token_list =[]
    token_count = []
    for temp_tuple in count_list:
        token_list.append(temp_tuple[0].strip())
        token_count.append(str(temp_tuple[1]))
    if False:
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print(count_list)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(token_list)
        token_list = np.unique(token_list)
        print('_____________________')
        print(token_list)
        #print(len(word_count))
        exit(0)
    #allwords_stemmed = [word for word in allwords_stemmed if word not in totalvocab_stemmed]
    token_str = ", ".join(token_list)
    count_str = ", ".join(token_count)

    #print(count_list)
    #print('------------------')

    #print(allwords_stemmed)
    #print(word_count)
    #print(allwords_stemmed_str)
    #print(word_count_str)
    #exit(0)
    data.insertToken(abstract_id, token_str, count_str)
    #totalvocab_stemmed.extend(allwords_stemmed_str)  # extend the 'totalvocab_stemmed' list
    #totalvocab_stemmed.append(allwords_stemmed_str)
    #allwords_tokenized = tokenize_only(i[1])
    #allwords_tokenized = [word for word in allwords_tokenized if word not in stopwords]
    #totalvocab_tokenized.extend(allwords_tokenized)
    if count%100 == 0:
        print(str(count))

exit(0)
#vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
#print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                    min_df=0.2, stop_words='english',
                    use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

tfidf_matrix = tfidf_vectorizer.fit_transform(synopses)
tfidf_array=tfidf_matrix.toarray();


#print(tfidf_matrix.shape)
print(tfidf_matrix.shape)
terms = tfidf_vectorizer.get_feature_names()
#print(len(terms))
dist = 1 - cosine_similarity(tfidf_matrix)



num_clusters = 5

km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

#

#std_dist_list = []
#for tempList in dist:
#    std_dist_list.append(np.std(tempList))

#print(dist)
    #tokenize_list = tokenize_and_stem(sentence)
#print(tokenize_list)
#tokens =nltk.word_tokenize(sentence)

#print(stopwords)
