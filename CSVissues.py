"""
Exports open issues from a specified repository to a CSV file
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""

import csv
import requests

# Commands for viewing issues in the command line:
# curl https://api.github.com/repos/devhub/dhplatform/issues?state=open&page=1 -u USERNAME
# #prompt for password#: PASSWORD

def write_issues(response): # method for writing all the issues on a page
    if not response.status_code == 200:
        raise Exception(response.status_code)
    for issue in response.json():
        if issue['state'] == "open":
            csvout.writerow([issue['number'], issue['title'].encode('utf-8'), issue['body'].encode('utf-8'), issue['created_at'], issue['updated_at']])

githubUser = '' ### ENTER USERNAME HERE
githubPass = '' ### ENTER PASSWORD HERE
repo = '' ### ENTER REPO HERE  # format is username/repo
csvfile = '%s-issues.csv' % (repo.replace('/', '-')) # creates file
csvout = csv.writer(open(csvfile, 'wb')) # opens file
csvout.writerow(('Id', 'Title', 'Body', 'Created At', 'Updated At')) # writes the header line

for page in range(0,15): # for each page you want to call to write all the issues
    pageStr = str(page+1)
    url = 'https://api.github.com/repos/%(x)s/issues?state=open&page=%(y)s' % {"x":repo, "y":pageStr}
    author = (githubUser, githubPass)
    r = requests.get(url, auth=author)
    write_issues(r)
