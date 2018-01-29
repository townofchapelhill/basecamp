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
request = requests.get("https://3.basecampapi.com/3472161/projects.json", headers={
    "Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
})
  
# set json file to variable
jfile = json.loads(request.text)

# intialize lists for projects & teams
p = []
t = []

# go through json and add to appropriate lists
for i in range(len(jfile)):

    if(jfile[i]["purpose"] == "topic"):
       p.append(jfile[i]["name"])
        
    if(jfile[i]["purpose"] == "team"):
        t.append(jfile[i]["name"])
        

# print lists    
print('Projects: ')
for proj in p:
    print(proj)
    
print('\nTeams: ')
for teams in t:
    print(teams)

# print program end timestamp
print('\n' + str(now))