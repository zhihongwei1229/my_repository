import numpy as np
import nltk
import re
from databaseConnection import Database
import string
from token_function import normalizeString,tokenize_and_stem,count_words,count_main_list

def insertTFIDF(data,TotalCountList):
    token_list = []
    tf_value_list = []
    affiliation_list = []
    for temp_tuple in TotalCountList:
        affiliation_list.append(str(temp_tuple[0]))
        token_list.append(temp_tuple[1].strip())
        tf_value_list.append(str(temp_tuple[2]))
    token_str = ",".join(token_list)
    tf_str = ",".join(tf_value_list)
    affiliation_str= ",".join(affiliation_list)
    data.insertAffiliationToken(affiliation_str, token_str,',', tf_str)
    print("inserted %s tokens into database" % str(len(token_list)))



data = Database()
stopwords = nltk.corpus.stopwords.words('english')
synopses = data.getAffiliation()

affiliation_list=[]
TotalCountList = []
count=0
for i in synopses:
    count += 1
    affiliation_id = i[0]
    content = normalizeString(i[1])
    allwords_stemmed = tokenize_and_stem(content)
    #print(allwords_stemmed)
    allwords_stemmed = [word for word in allwords_stemmed if word not in stopwords]
    #print(allwords_stemmed)
    count_list = count_words(allwords_stemmed)
    for token_count in count_list:
        temp_tuple=[]
        temp_tuple.append(affiliation_id)
        temp_tuple.append(token_count[0].strip())
        temp_tuple.append(str(token_count[1]))
        TotalCountList.append(temp_tuple)


    if((count%200)==0):
        print(TotalCountList)
        insertTFIDF(data,TotalCountList)
        TotalCountList=[]
insertTFIDF(data,TotalCountList)
exit(0)