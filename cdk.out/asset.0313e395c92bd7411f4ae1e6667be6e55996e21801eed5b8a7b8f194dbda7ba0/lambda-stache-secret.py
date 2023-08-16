import boto3
import json
import urllib.request
from botocore.exceptions import ClientError

#######################################

def lambda_handler(event,context):

    secret_name = "test/rds/aws"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name) # get the secret value from secret manager
    secret = get_secret_value_response['SecretString'] # store it into a variable as a string
    
    
    
    input_string = secret
    database_info = json.loads(input_string) #convert the string to a json ( as a dictionary )
   
    data_info = {
        "nickname" : "testing",
        "secret" : database_info["password"]
    }
    
# store the api value and stache api key.

    api_url = 'https://stache.utexas.edu/api/v2/entry/a78a81659794ca1ec59d3674281d028c/data/edit'
    STACHE = "fda526831d81026c6fcba88d52ad78947fbc6b3e0ac9c4bb112d088639c11efc" # this will be encrypted in the env variables
    
    headers = {
        'Content-Type': 'application/json',
        'X-STACHE-KEY': '10f639df53a7e977ec70ca55cbe37392b7c490a3eccbf74eb1a1774a31f6be23'
    }
    
    try:
        jsonData = json.dumps(data_info).encode('utf-8')
        req = urllib.request.Request(api_url, data=jsonData, headers=headers, method='POST') #send the data to STACHE
        

        with urllib.request.urlopen(req) as response:
            response_data= response.read().decode('utf-8')
            api_response = json.loads(response_data)
            return {
                'statusCode' : 200,
      #          'body': json.dumps(api_response, indent=4)
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e) #prompt the error.
        }
    
    return {
        'statusCode': 200
    }