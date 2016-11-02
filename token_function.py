from nltk.stem.snowball import SnowballStemmer
import nltk
import re
import unicodedata
import string


def remove_accents(data):
    valid_string =  string.ascii_letters+'1234567890'
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in valid_string).lower()

def tokenize_and_stem(text):
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer('english')
    tokens= [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    tokens = [word for word in tokens if word not in stopwords]

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