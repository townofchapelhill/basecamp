######################################################
##This script posts all schedule entries in the     ##
##Friendly Robot account's teams into the Automation##
##for the people's schedule                         ##
######################################################

import requests
import json
import csv
import datetime
import secrets

now = datetime.datetime.now()

# print program start timestamp
print(str(now) + '\n')

# use token and send request to get json response of projects & teams
token = secrets.basecamp_access

# access list of projects for account associated with token
project_url = "https://3.basecampapi.com/3472161/projects.json"
request = requests.get(project_url, headers={
    "Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
})
  
# set json file to variable
projects = json.loads(request.text)

# go through projects
for i in range(len(projects)):
    print(projects[i]["name"])
    if projects[i]["name"] == "Automation For The People":
        continue
    
    entry_url = projects[i]["dock"][3]["url"][:-5]+"/entries.json"
    request2 = requests.get(entry_url, headers={
        "Authorization": "Bearer " + token,
        "User-Agent": "ToCH Basecamp Integration (snguyen@townofchapelhill.org)"
    })

    entries = json.loads(request2.text)

    for j in range(len(entries)):
        print('\t' + entries[j]["title"])
        
        url = "https://3.basecampapi.com/3472161/buckets/6505832/schedules/899540291/entries.json"
        payload = {
          "summary" : entries[j]["summary"],
          "starts_at": entries[j]["starts_at"],
          "ends_at": entries[j]["ends_at"],
          "description": entries[j]["description"],
        #   "participant_ids": [10106580],
          "all_day": entries[j]["all_day"],
        }
        headers = {"Authorization": "Bearer " + token,
            "User-Agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)",
            "Content-Type":"application/json"}
        
        request = requests.post(url, data=json.dumps(payload), headers=headers)
  
print('\n' + str(datetime.datetime.now()))

