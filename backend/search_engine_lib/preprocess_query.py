import json
from search_engine_lib.retrieval_model import BM25
# from retrieval_model import Query_Likelihood

# helper functions
def removeD(word):
    res = list()
    lw = len(word)
    phrase = ''
    curr = ''
    sl = 0
    for i in range(lw):
        if word[i] != '.':
            curr += word[i]
            sl += 1
        else:
            if sl == 1:
                sl = 0
                phrase += curr
                curr = ''
                continue
            else:
                res.extend([phrase, curr] if len(phrase) >= 1 else [curr])
                curr = ''
                phrase = ''
    if len(phrase) >= 1:
        res.append(phrase)
    if len(curr) >= 1:
        res.append(curr)
    return res

def tokenize(lines):
    words = list()
    # split by space
    # tokenize
    for line in lines:
        word = ''
        for c in line:
            if c.isalpha():
                word += c.lower()
            elif c.isdigit() or c == '.':
                word += c
            else:
                if len(word) >= 1:
                    words.extend(removeD(word))
                word = ''
        if len(word) >= 1:
            words.extend(removeD(word))
    
    # read stopwords list
    stopwords = dict()
    with open('search_engine_lib/stopwords.txt', 'r') as f:
        stop_w = f.read().split('\n')
        for word in stop_w:
            stopwords[word] = True
    
    # return processed result (remove stopwords)
    return [word for word in words if stopwords.get(word) == None]

def query(queries, indexing_path, collection_path):
    inv_ind = None
    docs = None
    with open(indexing_path, 'r') as f:
        inv_ind = json.load(f)
    with open(collection_path, 'r') as f:
        docs = json.load(f)
    queries = tokenize([queries])
    print("queries", queries)

    model = BM25(k1=1.1, k2=10, b=0.6, inv_ind = inv_ind, docs=docs)
    #model = Query_Likelihood(mu=1000, inv_ind = inv_ind, docs=docs)

    retrieved_list = model.queries(queries)
    return retrieved_list

'''
function run, take queries as input, output the retrieved_list
'''

def run(queries):
    # fetch the stored docs and indexing
    indexing_path = 'search_engine_lib/stored/indexing.json'
    collection_path = 'search_engine_lib/stored/collection.json'
    data_path = 'search_engine_lib/stored/list.json'
    
    # perform retrieving tasks
    docs_list = list()
    if queries in ["blogs", "documentations", "reports"]:
        data = None
        with open(data_path, 'r') as f:
            data = json.load(f)
        docs_list = data[queries]
    else:    
        retrieved_list = query(queries, indexing_path, collection_path)
        for i in retrieved_list:
            docs_list.append(i["obj"])
    
    return docs_list