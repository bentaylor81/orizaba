from django.conf import settings
from django.shortcuts import render
import requests
import json

### SHIPTHEORY TOKEN ###
# REFRESH THE BEARER TOKEN AND ADD TO CONFIG VARS IN HEROKU
def shiptheory_token_task(request):
    # Generate the Auth Token
    url = settings.ST_URL_TOKEN
    payload='{"email": "'+settings.ST_USERNAME+'", "password": "'+settings.ST_PASSWORD+'"}'
    response = requests.request("POST", url, headers=settings.ST_HEADERS, data=payload)
    token = json.loads(response.text)['data']['token']
    heroku_token = 'Bearer ' + token
    # Update Heroku with Config Vars
    url = settings.HEROKU_URL_CONFIG_VARS
    auth = settings.HEROKU_BEARER_TOKEN
    payload='{"ST_AUTH":"'+heroku_token+'"}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.heroku+json; version=3', 'Authorization': auth, }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print("Task Ran!")

def hook_after_sleeping(task):
    print(task.result)

