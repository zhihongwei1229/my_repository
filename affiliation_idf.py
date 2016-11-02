from databaseConnection import Database
import math


data = Database()
affiliation_count = data.getAffiliationCount()
total_token_data = data.loadAffiliationTokens()

token_list=[]
idf_list=[]
for temp_tuple in total_token_data:

    token = temp_tuple[0]
    df = temp_tuple[1]
    idf = math.log(affiliation_count / df, 10)
    idf = round(idf, 4)
    if (idf < 0.0001):
        idf = 0.0001
    token_list.append(str(token))
    idf_list.append(str(idf))
    if(len(token_list) == 1000):
        token_str = ",".join(token_list)
        idf_str = ",".join(idf_list)
        data.updateAffiliationIdfValue(token_str, idf_str)
        token_list = []
        idf_list = []
        print('update %s idf_value as: %s' % (token, str(idf)))
        print('-------------------')