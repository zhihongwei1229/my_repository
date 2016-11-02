from databaseConnection import Database
import math

data = Database()
total_abstract_count = data.getDistinctAbstractNumberForTA('Family Medicine & Internal Medicine')

token_df_info =  data.loadTokenTable(total_abstract_count, 0.2, 0.001)
#print("total abstract count: " + str(total_abstract_count))

token_list = []
idf_list = []
count=0

for temp_tuple in token_df_info:
    count += 1
    token_list.append(str(temp_tuple[0]))

    df = temp_tuple[1]
    idf = math.log(total_abstract_count/df, 10)
    idf = round(idf, 4)
    if(idf <0.0001):
        idf = 0.0001
    idf_list.append(str(idf))

    if (len(token_list) == 1000):
        idf_str = ",".join(idf_list)
        token_str = ",".join(token_list)
        #print(idf_str)
        #print(token_str)
        token_list = []
        idf_list = []
        data.insertIdf(token_str, idf_str)
        print("-----------")
        print(count)

if(len(token_list)>0):
    idf_str = ",".join(idf_list)
    token_str = ",".join(token_list)
    token_list = []
    idf_list = []
    data.insertIdf(token_str, idf_str)

exit(0);