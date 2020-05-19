import json
from search_engine_lib.preprocess_and_indexing import preprocess, inverted_index

def preprocessing(stored_docs_path, indexing_path, collection_path):
    # fetch stopwords
    stopwords = list()
    with open('search_engine_lib/stopwords.txt', 'r') as f:
        stopwords = f.read()
        stopwords = stopwords.split('\n')
        stopwords.pop()

    # fetch json file of the documents
    data = None
    with open(stored_docs_path, 'r') as f:
        data = json.load(f)

    # tokenize, stopwords removal, stemming
    tokenize = preprocess(stopwords, data) # tokenize.text, map: ind -> [obj, [text]]
    tokenize.pre_process()
    tokenize.stemming()
    tokenize.stopword_removel()
    inv_ind = inverted_index(tokenize.text).inv_ind # map: term -> map: doc_ind -> list of positions

    with open(indexing_path, 'w') as f:
        json.dump(inv_ind, f)
    
    with open(collection_path, 'w') as f:
        json.dump(tokenize.text, f)

    # # check
    # inv_ind = None

    # with open(indexing_path, 'r') as f:
    #     inv_ind = json.load(f)
    # for term in inv_ind:
    #     print(term)
    #     print(inv_ind[term])
    #     print(' ')

    for i in tokenize.text:
        print("doc length: ", len(tokenize.text[i]["text"]))
    
if __name__ == '__main__':
    stored_docs_path = 'search_engine_lib/stored/list.json'
    indexing_path = 'search_engine_lib/stored/indexing.json'
    collection_path = 'search_engine_lib/stored/collection.json'
    preprocessing(stored_docs_path, indexing_path, collection_path)