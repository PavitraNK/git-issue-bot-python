# fetch list of issues
from github import Github
import os
#
token = os.getenv('GITHUB_TOKEN', '..')
# g = Github(token)
# repo = g.get_repo("PavitraNK/git-issue-bot-python")
# issues = repo.get_issues(state="open")
# print(issues.get_page(0))

# fetch issues
import requests
import os
from pprint import pprint

token = os.getenv('GITHUB_TOKEN', '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')
owner = "PavitraNK"
repo = "git-issue-bot-python"
query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
params = {
    "state": "open",
}
headers = {'Authorization': f'token {token}'}
r = requests.get(query_url, headers=headers, params=params)
issue_details= r.json()

print("Issue number: ",issue_details[0].get("number"))
print("Issue title: ",issue_details[0].get("title"))
print("Issue created date: ",issue_details[0].get("created_at"))
print("Issue body: ",issue_details[0].get("body"))
if issue_details[0].get("closed_at") == None:
    print("Issue Status: Open")
else:
    print("Issue Status: Closed")

# create issues
g = Github(token)
repo = g.get_repo("PavitraNK/git-issue-bot-python")
i = repo.create_issue(
    title="Issue Title",
    body="Text of the body.",
    assignee="PavitraNK",
    labels=[
        repo.get_label("good first issue")
    ]
)
pprint(i)