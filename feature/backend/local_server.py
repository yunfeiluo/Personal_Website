from flask import Flask
import json
from flask_cors import CORS, cross_origin
 
app = Flask(__name__)
CORS(app)
 
@app.route('/<user>')
def hello_world(user):
    jsonResp = {"query": user}
    return jsonResp
 
if __name__ == '__main__':
    app.run()