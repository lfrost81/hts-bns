from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from beans import Beans, Bean

field = [
    ("DOCID", "docid", "text", "primary key"), \
    ("DATE", "date", "int"), \
    ("URL", "url", "text"), \
    ("CATEGORY", "category", "text"), \
    ("TITLE", "title", "text"), \
    ("SNIPPET", "snippet", "text"), \
    ("CONTENT", "content", "text"), \
    ("SEQ", "token", "text") \
    ]

if __name__ == '__main__' :
    print("=" * 10 + "topic analysis start" + "=" * 10)

    bean = Beans()
    bean.init("./data/beans_komoran", field, False)

    bean.read_file()

    result = bean.executeQuery("select token from document")

    documents = [ list(c) for c in zip(*result) ][0]

    print (documents[0])

    texts = []
    for doc in documents :
        texts.append( doc.split() )

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary( texts )

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=20)

    print ( ldamodel.get_document_topics(dictionary.doc2bow(texts[0]) ) )

    print("=" * 10 + "topic analysis end" + "=" * 10)