import json
import boto3

# fetch docs from database
db = boto3.resource('dynamodb')
table = db.Table('article')

s3 = boto3.client('s3')

# helper functions
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key'] # it is the path in the bucket
    print(file_name)
    
    id_ = 1
    while True:
        item = table.get_item(Key={"id":id_})
        if item.get("Item") == None:
            break
        id_ += 1
    
    item = {
        "id": id_, 
        "type": "",
        "title": "",
        "tags": list(),
        "path": file_name,
        "summery": "", 
        "docs": list()
    }
    
    table.put_item(Item=item)
        
    # response
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
