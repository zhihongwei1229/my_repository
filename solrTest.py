from solr import *
import pysolr

#conn = solr.solr("http://solr.example.net/solr")
#conn = solr.Solr("http://solr.example.net/solr")
#solr.SearchHandler(conn,"/select")
#conn.query()
import sklearn
from SolrClient import SolrClient

solr=SolrClient('http://192.168.1.100:8983/solr/')

result=solr.query('tableAbstract',{'q':'memBody:blood','facet':True,'facet.range.start':0,'facet.range.end':1000000})
for x in result.docs:
    #print(x['id'])
    print(int(float(x['id'])))
    #print(x['id'])
print (result.get_num_found())