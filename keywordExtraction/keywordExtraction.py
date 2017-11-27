# -*- encoding:utf-8 -*-

import os
import copy
import glob
import sys

from konlpy.tag import Twitter
from nltk import regexp_tokenize

pos_tagger = Twitter()
def tokenize(doc):
    # norm, stem은 optional
    # 한글자 이상, 명사,동사,형용사 만 추출
    return " ".join(["%s/%s" % (t[0], t[1][0]) for t in pos_tagger.pos(doc, norm=True, stem=True) if t[1] in "|Noun|Verb|Abjective|" and len(t[0]) > 1 ] )

from konlpy.tag import Komoran
komoran = Komoran()

def tokenize_komoran( doc ) :
    return " ".join(["%s/%s" % (t[0], t[1][0:2]) for t in komoran.pos(doc) if t[1] in "|NNP|NNG|VA|VV|" and len(t[0]) > 1 ] )
###
###
###
def save_to_file(docs, target_file_path):
    print(len(docs))

    with open(target_file_path, "w") as ofs:
        for index in range(0, len(docs)):
            document = docs[index]
            ofs.write("DOCID::=hcdf_%s\n" % str(index).zfill(8))
            ofs.write("DATE::=\n")
            ofs.write("URL::=%s\n" % document[0])
            ofs.write("CATEGORY::=%s\n" % document[1])
            ofs.write("TITLE::=%s\n" % document[2])
            ofs.write("SNIPPET::=%s\n" % document[3])
            ofs.write("CONTENT::=%s\n" % document[4])
            ofs.write("SEQ::=%s\n" % document[5])
            ofs.write("\n")


###
###
###
def formatter(files):
    docs = []
    doc = []

    for file in files:
        with open(file, "r") as f:
            for line in f:
                del (doc[:])

                temp = line.replace('\xa0', ' ').split('\t')

                if len(temp) < 3:
                    print(temp)

                doc.append(temp[-1].strip())  # url
                doc.append(temp[0].strip())  # category
                doc.append(temp[1].strip())  # title
                doc.append(temp[2].strip())  # snippet
                doc.append("\t".join(temp[3:-1]).strip())  # content
                doc.append("%s _SEP_ %s" % (tokenize_komoran(temp[0]), tokenize_komoran("\t".join(temp[3:-1]))))  # keyword

                docs.append(copy.deepcopy(doc))

    return docs

if __name__ == '__main__':
    print("=== play tokenize ====")

    source_path = "./data/raw/source/"
    target_file = "./data/raw/target/documents.hcdf"

    docs = formatter( glob.glob( os.path.join( source_path, "*.*" ) ) )
    #save_to_file( docs, target_file )


