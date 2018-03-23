import requests
import json
import csv
import datetime
import secrets

now = datetime.datetime.now()

# https://3.basecampapi.com/3472161/buckets/6505832/chats/899540284/lines.json
# api testing: https://3.basecampapi.com/3472161/buckets/6806445/chats/943497859/lines.json

# print program start timestamp
print(str(now) + '\n')

# use token and send request to get json response of projects & teams
token = secrets.basecamp_access

project_url = "https://3.basecampapi.com/3472161/projects.json"
request = requests.get(project_url, headers={
    "Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
})
  
# set json file to variable
projects = json.loads(request.text)

message = "Schedule Entries: \n"

# go through projects
for i in range(len(projects)):
    
    message += str(i+1) + ". " + projects[i]["name"] + '\n'
    entry_url = projects[i]["dock"][3]["url"][:-5]+"/entries.json"
    request2 = requests.get(entry_url, headers={
        "Authorization": "Bearer " + token,
        "User-Agent": "ToCH Basecamp Integration (snguyen@townofchapelhill.org)"
    })
    
    entries = json.loads(request2.text)
    
    for j in range(len(entries)):
        message += '\t'+ entries[j]["title"] + " - " + entries[j]["starts_at"] + '\n'
    
print(message)

url = "https://3.basecampapi.com/3472161/buckets/6505832/chats/899540284/lines.json"
payload = {"content": message}
headers = {"Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)",
    "Content-Type":"application/json"}

request = requests.post(url, data=json.dumps(payload), headers=headers)
  
# set json file to variable
jfile = json.loads(request.text)

print(jfile)
print('\n' + str(datetime.datetime.now()))

