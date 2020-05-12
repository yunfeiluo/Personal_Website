import json
from feature.search_engine.retrieval_model import Query_Likelihood, BM25

# remove the dot '.' in the string, return string
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
    return words

def query(queries_path, indexing_path, collection_path):
    inv_ind = None
    docs = None
    queries = None
    with open(indexing_path, 'r') as f:
        inv_ind = json.load(f)
    with open(collection_path, 'r') as f:
        docs = json.load(f)
    with open(queries_path, 'r') as f:
        queries = json.load(f)
    queries = tokenize(queries)

    model = BM25(k1=1.1, k2=10, b=0.6, inv_ind = inv_ind, docs=docs)
    #model = Query_Likelihood(mu=1000, inv_ind = inv_ind, docs=docs)

    retrieved_list = model.queries(queries)
    return retrieved_list

if __name__ == '__main__':
    collection_path = 'articles/collection.json'
    indexing_path = 'articles/indexing.json'
    queries_path = 'articles/queries.json'
    
    retrieved_list = query(queries_path, indexing_path, collection_path)

    # check / output
    for i in retrieved_list:
        print(i["obj"]["title"])
        