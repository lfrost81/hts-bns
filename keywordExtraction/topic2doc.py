import os
import sys

# 1. get docid by topic id
docid2topicid = dict()

with open( "./data/id2topic") as f :
    for line in f:
        item = line.strip().split('|')

        id = item[0]
        weights = [ float( weight ) for weight in item[1].split(',') ]

        temp = sorted( [ (v,i) for i,v in enumerate( weights ) ], reverse=True )

        docid2topicid[id] = set([ t[1] for t in temp if t[0] > 0.3 ])

#print( docid2topicid )

id2name = dict()

with open("./data/id2name") as f:
    for line in f:
        item = line.strip().split('|')
        id2name[item[0]] = item[1]

#print( id2name )


###
keyword2name = dict()

with open("./data/merchant2.txt") as ifs_m2k:
    for line in ifs_m2k:
        item = line.strip().split('\t')
        keyword2name[item[1].strip()] = item[0].strip()

#print(keyword2name)

def getBaseMerchantName(keyword):
    return keyword2name[keyword.strip()]

def getMerchantName(mid):
    return getBaseMerchantName(id2name[mid])

### make
merchantListByTopic = [None]*10

for i in range( 0, 10 ) :
    merchantListByTopic[i] = set()

for docid, topicid in docid2topicid.items():

    try :
        mname = getMerchantName( docid )
    except :
        continue

    for id in topicid :
        merchantListByTopic[id].add(getMerchantName(docid))

labelByTopic = [ "합리주의","식도락가","스타일리쉬","대중적인","사회적인","얼리어댑터","커피홀릭","연예인병","웰빙족","패셔너블한" ]
for i in range( 0, 10 ) :
    print( labelByTopic[i] , merchantListByTopic[i] )


with open( "../data/merchantWithTopicByLDA.txt", "w" ) as f :
    for i in range( 0, 10 ) :
        for merchant in merchantListByTopic[i] :
            f.write( "%s,%s,1\n" % ( merchant , labelByTopic[i] ) )

sys.exit()
