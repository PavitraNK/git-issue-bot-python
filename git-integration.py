from github import Github
import os
from collections import Counter
import requests
import os
from pprint import pprint
import nltk
from stop_words import get_stop_words
from nltk.corpus import stopwords
# declarations
issue_title_list= []
issue_number_list = []
issue_number_title= []
issue_assignee = []
match_issue_list =[]
username_list= {}
# Github token and
token = os.getenv('GITHUB_TOKEN', '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')
headers = {'Authorization': f'token {token}'}
owner = "PavitraNK"
repo = "git-issue-bot-python"

# fetch list of issues
query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
params = {
    "state": "all",
}
r = requests.get(query_url, headers=headers, params=params)
issue_details= r.json()
for each_issue in range(len(issue_details)):
    issue_number_title= str(issue_details[each_issue].get("number"))+". "+issue_details[each_issue].get("title")
    issue_title_list.append(issue_number_title)
    issue_number_list.append(issue_details[each_issue].get("number"))
    if issue_details[each_issue].get("closed_at") == None:
        issue_assignee.append(issue_details[each_issue].get("assignee").get('login'))

if issue_title_list:
    print("issue_title_list:", issue_title_list)
    print("issue_number_list:", issue_number_list)
else:
    print("Seems, Related issues not found. Please report this as a new issue")

#search original input in issue list
original_user_input= "I am facing dashboard issue that is not good"
for each_issue in range(len(issue_title_list)):
    if original_user_input.lower() in issue_title_list[each_issue].lower():
        match_issue_list.append(issue_title_list[each_issue])

#Search filtered keywords from user input in issue list. Keyword extraction
# logic added through Natural language toolkit

# Find out stop words and natural words
stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))
stop_words.extend(nltk_words)
#Tokenized original user input
tokens=nltk.word_tokenize(original_user_input)
print(tokens)
search_words = []
# Removed stop words and other ntlk words from tokenized user input
for words in tokens:
    if not words.lower() in stop_words:
        search_words.append(words.lower())

print("serach words:", search_words)
# Removed some common words from tokenized user input
some_common_words_for_manual_removal = ["issue", "problem", "faced", "facing", "good", "bad"]
for each_word in some_common_words_for_manual_removal:
    if each_word in search_words:
        search_words.remove(each_word)

print("search words:", search_words)

for each_word in search_words:
    for each_issue in range(len(issue_title_list)):
        if each_word.lower() in issue_title_list[each_issue].lower():
            match_issue_list.append(issue_title_list[each_issue])
print("Matching issue: ", match_issue_list)

#show details of issue from issue number
issue_number = 3
if issue_number in issue_number_list:
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    r = requests.get(query_url, headers=headers)
    issue_details = r.json()
    pprint("Please find issue details below:")
    print("Issue Number: ",issue_details.get("number"))
    print("Issue Title: ",issue_details.get("title"))
    print("Issue created date: ",issue_details.get("created_at"))
    print("Issue body: ",issue_details.get("body"))
    if issue_details.get("closed_at") == None:
        print("Issue status is Open. This issue is in progress.")
    else:
        print("Issue Status is Closed. This issue is already fixed and will be available in next software update")
else:
    print("Please enter valid issue number")

# Get collaborators/assignee
# Check number of issues assigned to each collaborators
# will assign to collaborator who has less issues assigned
query_url = f"https://api.github.com/repos/{owner}/{repo}/collaborators"
r = requests.get(query_url, headers=headers)
users_list = r.json()
#find out total users and form dict of them with value 0
for each_user in range(len(users_list)):
    username_list[users_list[each_user].get('login')] =0

#find out how many issues assigned to each user  from list of issues
number_of_issues_assigned = Counter(issue_assignee)

# merge two above dicts
for key,value in number_of_issues_assigned.items():
    if key in username_list:
        username_list[key] = value
print("issue_assignee:", issue_assignee)
print("number_of_issues_assigned:", number_of_issues_assigned)
print("username_list:", username_list)

#find out assignee who has minimum issues assigned
assignee = min(username_list, key=username_list.get)
print("assignee:", assignee)

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


#User input validation
user_input='N'
users_predefined_input1 = ['y', 'n','yes', 'no']
if user_input.lower() in  users_predefined_input1:
    print("Entered valid input")
    # Add code here to proceed and ask user about issue details
else:
    print("Please enter input in form of y|yes|n|no")