import json
from feature.search_engine.tokenize import preprocess
from feature.search_engine.indexing import inverted_index
import feature.search_engine.retrieval_model as model

if __name__ == '__main__':
    # fetch stopwords
    stopwords = list()
    with open('feature/search_engine/stopwords.txt', 'r') as f:
        stopwords = f.read()
        stopwords = stopwords.split('\n')
        stopwords.pop()

    # fetch json file of the documents
    data = None
    with open('articles/list.json', 'r') as f:
        data = json.load(f)

    # tokenize, stopwords removal, stemming
    tokenize = preprocess(stopwords, data) # tokenize.text, map: ind -> [obj, [text]]
    tokenize.pre_process()
    tokenize.stemming()
    tokenize.stopword_removel()
    inv_ind = inverted_index(tokenize.text).inv_ind # map: term -> map: doc_ind -> list of positions

    # check
    # for term in inv_ind:
    #     print(term)
    #     print(inv_ind[term])
    #     print(' ')
    # for i in tokenize.text:
    #     print(len(tokenize.text[i][1]))
    
