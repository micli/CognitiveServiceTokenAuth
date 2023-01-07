import re, os
import requests
from datetime import datetime

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()
endpoint = ''
key = ''
token = ''

def output_information():
    print('Azure Cognitive Service Token Retrieval Sample')
    print('---------------------------------------------')
    print('This application only demonstrate a very simple layer to protect cognitive service key to distribute to clients.')
    print('It distributes token rather than key. Token only used by connecting to Azure Cognitive Service at beginning. Once connected,token will not be required.')
    print('If you want to leverage code, please make authentication protect on get_cs_token() method.')

def init():
    endpoint = os.environ.get('COGNITIVE_SERVICE_ENDPOINT', None)
    key = os.environ.get('COGNITIVE_SERVICE_KEY', None)
    if endpoint is None or key is None:
        raise Exception('COGNITIVE_SERVICE_ENDPOINT and COGNITIVE_SERVICE_KEY must be set.')
    
    output_information()
    # set a background task to retrieve cognitive service token every 5 minutes.
    scheduler.add_job(func=retrieve_token, args=(app, endpoint, key),id="id_retrieve_token", trigger="interval", seconds=300, replace_existing=False)
    scheduler.start()
    return endpoint, key

# retrieve cognitive service token by requests every 5 minutes
def retrieve_token(app, endpoint, key):
    with app.app_context():
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': key,
            'Content-length': '0'
        }
        response = requests.post(endpoint, headers=headers)
        if response.status_code == 200:
            global token
            token = response.text
            return jsonify({'token': token})
        else:
            return None


endpoint, key = init()
retrieve_token(app, endpoint, key)

@app.route('/')
def home():
    return "Get cognitive service authentication token."


@app.route('/token/', methods=["GET"])
def get_cs_token():
    return jsonify({'token': token})



if __name__ == "__main__":
    endpoint, key = init()
    retrieve_token(app, endpoint, key)
    app.run(host='0.0.0.0', port=5000, debug=True)