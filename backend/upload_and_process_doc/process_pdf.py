import json
import sys

if __name__ == '__main__':
    # 1 is type, 2 is name
    type_ = sys.argv[1]
    file_name = sys.argv[2]
    
    txt_filename = "../articles/{}s/{}.txt".format(type_, file_name)

    json_file = {
        "id": -1, 
        "type": type_,
        "title": ".", 
        "path": "articles/{}s/{}.pdf".format(type_, file_name),
        "docs": list(),
        "tags": list(),
        "summery": ".",
        "text": "."
    }

    text = None
    with open(txt_filename, 'r') as f:
        text = f.read()
    
    json_file["text"] = text

    with open("../articles/{}s/{}.json".format(type_, file_name), 'w') as f:
        json.dump(json_file, f)
        