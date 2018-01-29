import requests
import json
import csv
import datetime
import secrets

now = datetime.datetime.now()

# print program start timestamp
print(str(now) + '\n')

# use token and send request to get json response of todo sets
token = secrets.basecamp_access
request = requests.get("https://3.basecampapi.com/3472161/buckets/2528552/todosets/365963496/todolists.json", headers={
    "Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
})

# set json file to variable
todo_set = json.loads(request.text)

# go through json todo sets, skipping completed sets
for i in range(len(todo_set)):
    
    if todo_set[i]["completed"]:
        continue
    
    # print name of todo set
    print(todo_set[i]["name"])
    
    # use token again to get json todo list of current todo set
    request = requests.get(todo_set[i]["todos_url"], headers={
        "Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    })
    
    # set json todo list to variable
    todo_list = json.loads(request.text)
    
    for i in range(len(todo_list)):
        print("---> " + todo_list[i]["content"])
    
    print('\n')

print(str(now))