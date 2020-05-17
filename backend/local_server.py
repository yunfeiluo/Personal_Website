import json
from flask import Flask
from flask_cors import CORS, cross_origin

import search_engine_lib.preprocess_query as pq
 
app = Flask(__name__)
CORS(app)

@app.route('/<queries>')
def fetch_docs(queries):
    # queries = event["query"] # aws lambda
    
    docs_list = pq.run(queries)
    
    # return response
    return {
        "docs_list": docs_list
    }
 
if __name__ == '__main__':
    app.run()