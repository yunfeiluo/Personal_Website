import json
from feature.search_engine.retrieval_model import Query_Likelihood, BM25

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

    #model = BM25(k1=1.1, k2=10, b=0.6, inv_ind = inv_ind, docs=docs)
    model = Query_Likelihood(mu=1000, inv_ind = inv_ind, docs=docs)

    retrieved_list = model.queries(queries)
    return retrieved_list

if __name__ == '__main__':
    collection_path = 'articles/collection.json'
    indexing_path = 'articles/indexing.json'
    queries_path = 'articles/queries.json'
    
    retrieved_list = query(queries_path, indexing_path, collection_path)

    # check
    for i in retrieved_list:
        print(i["obj"]["title"])