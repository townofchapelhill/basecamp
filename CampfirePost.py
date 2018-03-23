import requests
import json
import csv
import datetime
import secrets

now = datetime.datetime.now()

# https://3.basecampapi.com/3472161/buckets/6505832/chats/899540284/lines.json

# print program start timestamp
print(str(now) + '\n')

# use token and send request to get json response of projects & teams
token = secrets.basecamp_access

url = "https://3.basecampapi.com/3472161/buckets/6505832/chats/899540284/lines.json"
payload = {"content": "Hello World"}
headers = {"Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)",
    "Content-Type":"application/json"}

request = requests.post(url, data=json.dumps(payload), headers=headers)
  
# set json file to variable
jfile = json.loads(request.text)

print(jfile)
