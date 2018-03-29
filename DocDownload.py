import requests
import json
import datetime
import secrets

now = datetime.datetime.now()

# print program start timestamp
print(str(now) + '\n')

# use token and send request to get json response of projects & teams
token = secrets.basecamp_access

test_js = "https://3.basecampapi.com/3472161/buckets/6505832/uploads/904675583/download/foo.js"
request = requests.get(test_js, headers={
    "Authorization": "Bearer " + token,
    "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
})
  
with open('test.js', 'wb') as f:
    f.write(request.content)