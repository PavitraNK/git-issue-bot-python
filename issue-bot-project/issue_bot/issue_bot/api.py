import requests
from stop_words import get_stop_words
import nltk
from nltk.corpus import stopwords
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from github import Github
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import Counter
from .chatbot import chatbot

from .constants import REPO,REPO_OWNER,HEADERS,GIT_TOKEN
from .serializers import CreateIssueSerializer

class GetIssueLists(ListAPIView):

    def list(self, request):
        # fetch list of issues
        query_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO}/issues"
        params = {
            "state": "all",
        }
        r = requests.get(query_url, headers=HEADERS, params=params)
        issue_details= r.json()
        return Response(issue_details)

class GetIssueDetails(RetrieveAPIView):

    def retrieve(self,request,pk):
        # get issue details

        issue_number = self.kwargs.get('pk', None)

        query_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO}/issues/{issue_number}"
        r = requests.get(query_url, headers=HEADERS)
        issue_details = r.json()
        return Response(issue_details)



class CreateIssue(APIView):

    def issue_assignee_list(self):
        # find out all assignees present in git repo
        # Get collaborators/assignee
        issue_assignee=[]
        query_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO}/issues"
        params = {
            "state": "all",
        }
        r = requests.get(query_url, headers=HEADERS, params=params)
        issue_details= r.json()
        for each_issue in range(len(issue_details)):
            if issue_details[each_issue].get("closed_at") == None:
                issue_assignee.append(issue_details[each_issue].get("assignee").get('login'))
        return issue_assignee

    def get_assignee(self):
        # Check number of issues assigned to each collaborators
        # will assign to collaborator who has less issues assigned
        username_list= {}
        query_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO}/collaborators"
        r = requests.get(query_url, headers=HEADERS)
        users_list = r.json()
        #find out total users and form dict of them with value 0
        for each_user in range(len(users_list)):
            username_list[users_list[each_user].get('login')] =0

        #find out how many issues assigned to each user  from list of issues
        number_of_issues_assigned = Counter(self.issue_assignee_list())

        # merge two above dicts
        for key,value in number_of_issues_assigned.items():
            if key in username_list:
                username_list[key] = value

        #find out assignee who has minimum issues assigned
        return min(username_list, key=username_list.get)

    def post(self, request):
        serializer = CreateIssueSerializer(data=request.data)
        if serializer.is_valid():
            g = Github(GIT_TOKEN)
            repo = g.get_repo("PavitraNK/git-issue-bot-python")
            issue_details = repo.create_issue(
                title=serializer.data.get('issue_title'),
                body=serializer.data.get('issue_details'),
                assignee=self.get_assignee(),
                labels=[
                    repo.get_label("bug")
                ]
            )
            return Response({"issue_number":issue_details.number,"data":serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

class FilterIssue(APIView):

    def issue_list(self):
        issue_title_list=[]
        # fetch list of issues
        query_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO}/issues"
        params = {
            "state": "all",
        }
        r = requests.get(query_url, headers=HEADERS, params=params)
        issue_details= r.json()
        for each_issue in range(len(issue_details)):
            issue_number_title= str(issue_details[each_issue].get("number"))+". "+issue_details[each_issue].get("title")
            issue_title_list.append(issue_number_title)
        return issue_title_list

    def get(self, request, search_name=None):
        #search original input in issue list
        match_issue_list=set()
        original_user_input= search_name

        issue_list= self.issue_list()
        for each_issue in range(len(issue_list)):
            if original_user_input.lower() in issue_list[each_issue].lower():
                match_issue_list.add(issue_list[each_issue])

        #Search filtered keywords from user input in issue list. Keyword extraction
        # logic added through Natural language toolkit

        # Find out stop words and natural words
        stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
        nltk_words = list(stopwords.words('english'))
        stop_words.extend(nltk_words)
        #Tokenized original user input
        tokens=nltk.word_tokenize(original_user_input)

        search_words = []
        # Removed stop words and other ntlk words from tokenized user input
        for words in tokens:
            if not words.lower() in stop_words:
                search_words.append(words.lower())

        # Removed some common words from tokenized user input
        some_common_words_for_manual_removal = ["issue", "problem", "faced", "facing", "good", "bad"]
        for each_word in some_common_words_for_manual_removal:
            if each_word in search_words:
                search_words.remove(each_word)

        for each_word in search_words:
            for each_issue in range(len(issue_list)):
                if each_word.lower() in issue_list[each_issue].lower():
                    match_issue_list.add(issue_list[each_issue])
        return Response(match_issue_list)



class GetBotResponse(APIView):

    def get(self, request, message=None):
        userText = message
        return HttpResponse(str(chatbot.get_response(userText)))

# class GetChatHistory():
#
# class SaveChatHistory():