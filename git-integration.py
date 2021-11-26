# fetch list of issues
from github import Github
import os
from collections import Counter
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
    "state": "all",
}
headers = {'Authorization': f'token {token}'}
r = requests.get(query_url, headers=headers, params=params)
issue_details= r.json()
issue_title_list= []
issue_number_list = []
issue_assignee = []
for each_issue in range(len(issue_details)):
    issue_number_title= str(issue_details[each_issue].get("number"))+". "+issue_details[each_issue].get("title")
    issue_title_list.append(issue_number_title)
    issue_number_list.append(issue_details[each_issue].get("number"))
    if issue_details[each_issue].get("closed_at") == None:
        issue_assignee.append(issue_details[each_issue].get("assignee").get('login'))
#
# original_user_input= "login issue"
# match_issue_list =[]
#
# #search original input in issue list
# for each_issue in range(len(issue_title_list)):
#     if original_user_input in issue_title_list[each_issue]:
#         match_issue_list.append(issue_title_list[each_issue])
# #
# #Search filtered keywords from user input in issue list. Keyword extraction logic pending
# search_words=original_user_input.split()
# for each_word in search_words:
#     for each_issue in range(len(issue_title_list)):
#         if each_word in issue_title_list[each_issue]:
#             match_issue_list.append(issue_title_list[each_issue])
# print(match_issue_list)
# #show details of issue from issue number
# issue_number = 2
# if issue_number in issue_number_list:
#     query_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
#     r = requests.get(query_url, headers=headers)
#     issue_details = r.json()
#     pprint("Please find issue details below:")
#     print("Issue Number: ",issue_details.get("number"))
#     print("Issue Title: ",issue_details.get("title"))
#     print("Issue created date: ",issue_details.get("created_at"))
#     print("Issue body: ",issue_details.get("body"))
#     if issue_details.get("closed_at") == None:
#         print("Issue status is Open. This issue is in progress.")
#     else:
#         print("Issue Status is Closed. This issue is already fixed and will be available in next software update")
# else:
#     print("Please enter valid issue number")

# Get collaborators/assignee
# Check number of issues assigned to each collaborators
# will assign to collaborator who has less issues assigned
query_url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"
r = requests.get(query_url, headers=headers)
users_list = r.json()
username_list= {}
#find out total users and form dict of them with value 0
for each_user in range(len(users_list)):
    username_list[users_list[each_user].get('login')] =0

#find out how many issues assigned to each user  from list of issues
number_of_issues_assigned = Counter(issue_assignee)

# merge two above dicts
for key,value in number_of_issues_assigned.items():
    if key in username_list:
        username_list[key] = value

#find out assignee who has minimum issues assigned
assignee = min(username_list, key=username_list.get)

# create issues if user does not find
g = Github(token)
user_input_section = "Dashboard"
user_input_issue_title = "not able to click on message icon"
title = user_input_section + ': '+ user_input_issue_title
body = "steps: 1. Go to dashboard. 2. Click on message icon. Actual: Not able to click on message icon Expected: User should be able to click on message icon"
repo = g.get_repo("PavitraNK/git-issue-bot-python")
issue_details = repo.create_issue(
    title=title,
    body=body,
    assignee=assignee,
    labels=[
        repo.get_label("bug")
    ]
)
pprint(issue_details)
