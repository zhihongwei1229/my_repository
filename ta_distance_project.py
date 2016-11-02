from nltk.stem.snowball import SnowballStemmer
import numpy as np
import nltk
import re
from databaseConnection import Database
import unicodedata
import string

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

data = Database()
stopwords = nltk.corpus.stopwords.words('english')
synopses = data.getAbstractByTherapeuticArea('Family Medicine & Internal Medicine')

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
        data.insertTokenV1(abstract_str, token_str, df_str, tf_str)
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
    data.insertTokenV1(abstract_str, token_str, df_str, tf_str)
    print("inserted %s tokens into database" % str(len(token_list)))
exit(0)