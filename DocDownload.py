import requests
import json
import datetime
import secrets

# use token and send request to get json response of projects & teams
token = secrets.basecamp_access

# check vault function 
def check_vault(doc):
    # check if there are documents in each container
    # print(doc["documents_count"])
    # if doc["documents_count"] != 0:
    #     docs_url = doc["documents_url"]
    #     docs_request = requests.get(docs_url, headers ={
    #         "Authorization": "Bearer " + token,
    #         "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    #     })
    #     docs = json.loads(docs_request.text)
    #     print(len(docs))
    #     for j in range(len(docs)):
    #         print(j)
    #         download = requests.get(docs[j]["downloads_url"], headers={
    #             "Authorization": "Bearer " + token,
    #             "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    #         })
              
    #         with open(docs[j]["filename"], 'wb') as f:
    #             f.write(download.content)
    
    if doc["uploads_count"] != 0:
        uploads_url = doc["uploads_url"]
        upload_request = requests.get(uploads_url, headers ={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        uploads = json.loads(upload_request.text)
        
        for k in range(len(uploads)):
            download = requests.get(uploads[k]["download_url"], headers={
                "Authorization": "Bearer " + token,
                "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
            })
              
            with open(uploads[k]["filename"], 'wb') as f:
                f.write(download.content)
        
        
    if doc["vaults_count"] != 0:
        vaults_url = doc["vaults_url"]
        vaults_request = requests.get(vaults_url, headers ={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        vaults = json.loads(vaults_request.text)
        
        for l in range(len(vaults)):
            check_vault(vaults[l])

def main():            
    # get current timestamp
    now = datetime.datetime.now()
    
    # print program start timestamp
    print(str(now) + '\n')
    
    # access list of projects for account associated with token
    project_url = "https://3.basecampapi.com/3472161/projects.json"
    request = requests.get(project_url, headers={
        "Authorization": "Bearer " + token,
        "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
    })
    
    # set json file to variable
    projects = json.loads(request.text)
    
    # loop through projects/teams
    for i in range(len(projects)):
        print(projects[i]["name"])
        # access list of documents for account associated with token in team at index i
        doc_url = projects[i]["dock"][5]["url"]
        doc_request = requests.get(doc_url, headers={
            "Authorization": "Bearer " + token,
            "user-agent": "Town of Chapel Hill Basecamp Integration (snguyen@townofchapelhill.org)"
        })
        
        # set document json to variable
        documents = json.loads(doc_request.text)
        
        # call function to check vault
        check_vault(documents)

main()
