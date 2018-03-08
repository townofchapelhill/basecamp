import requests
import json
import csv
import datetime
import secrets

now = datetime.datetime.now()

# print program start timestamp
print(str(now) + '\n')

# open csv file
basecamp_bot = open('basecamp_bot.csv', 'w')
writer = csv.writer(basecamp_bot)
writer.writerow(['Team', 'Todo-set', 'To-do'])

# use token and send request to get json response of projects & teams
token = secrets.basecamp_access

# get project info
project_url = "https://3.basecampapi.com/3472161/projects.json"
request = requests.get(project_url, headers={
    "Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
})
  
# set json file to variable
projects = json.loads(request.text)

row = []

# go through projects
for i in range(len(projects)):
    
    if(projects[i]["purpose"] == "team"):
        row.append(projects[i]["name"])
        
        # get url for todosets
        todoset_url = projects[i]["dock"][2]["url"][:-5] + "/todolists.json"
        # print(url+"\n")
        request2 = requests.get(todoset_url, headers={
        "Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        
        todo_set = json.loads(request2.text)

        # go through json todo sets, skipping completed sets
        for j in range(len(todo_set)):
            
            if todo_set[j]["completed"]:
                continue
            
            # print name of todo set
            if not row:
                row.append("")
            row.append(todo_set[j]["name"])
            
            # use token again to get json todo list of current todo set
            request3 = requests.get(todo_set[j]["todos_url"], headers={
                "Authorization": "Bearer " + token,
                "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
            })
            
            # set json todo list to variable
            todo_list = json.loads(request3.text)
            
            if not todo_list:
                writer.writerow(row)
                row = []
                continue
            
            for k in range(len(todo_list)):
                if not row:
                    row.append("")
                    row.append("")
                row.append(todo_list[k]["content"])
                writer.writerow(row)
                row = []

basecamp_bot.close()

# print program end timestamp
print('\n' + str(now))
