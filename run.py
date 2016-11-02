# engine://user:password@host:port/database
from sqlalchemy import *
import xml.etree.ElementTree as ET
from vector import *
from vecterCalculate import *
from math import degrees
from string import *
from sys import *
import unicodedata
import string

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

normalized_token = remove_accents('frigorífico')
print(normalized_token)
exit(0)


sum = lambda var1, var2: var1+var2

print("value of total is: %d. " % (sum(20,1)))
exit(0)


print(degrees(acos(1/2) ))
print('\r')
print('      xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     '+"|||")
print(('      xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     ').strip()+"|||")
print("this is a string: %s, and this is a number: %d" % ("'free text'", 501))

list = [1,2,3]
for x in list:
    print(x)
for x in list:
    print(x, end='|')
exit(0)

my_vector =  Vector([-2.328,-7.284,-1.214])
new_vector = Vector([-1.821,1.072,-2.94])

#print(my_vector.dot(new_vector))
exit(0)


xml_string = '<?xml version="1.0"?><data> <country name="Liechtenstein"> <rank>1</rank><year>2008</year> <gdppc>141100</gdppc> <neighbor name="Austria" direction="E"/> <neighbor name="Switzerland" direction="W"/></country> <country name="Singapore"><rank>4</rank> <year>2011</year><gdppc>59900</gdppc><neighbor name="Malaysia" direction="N"/> </country><country name="Panama"> <rank>68</rank><year>2011</year> <gdppc>13600</gdppc><neighbor name="Costa Rica" direction="W"/><neighbor name="Colombia" direction="E"/> </country></data>'
root = ET.fromstring(xml_string)
for child in root:
    print (child.tag, child.attrib)

exit()








#engine = create_engine('mssql://sa:Sa_password_@_2013@10.30.2.23:1433/ProdMemeODS')
engine = create_engine('mssql+pymssql://sa:Sa_password_@_2013@10.30.2.23:1433/ProdMemeODS')
conn = engine.connect()
#engine.echo = True
param1 = "252"
#inspection = inspect(engine)

#result = conn.execute('select top(5) * from ssop.users where user_id= %s', (param1))
result = conn.execute('select search_info as search_info from impactmeme.Saved_Search_Setting where SAVED_SEARCH_ID=%s', (param1))

for row in result:
    print(row['search_info'])
#c.execute("SELECT * FROM foo WHERE bar = %s AND baz = %s", (param1, param2))

#print(inspection.get_table_names("conferencememe"))