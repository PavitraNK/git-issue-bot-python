import os


REPO_OWNER = "PavitraNK"
REPO = "git-issue-bot-python"

GIT_TOKEN = os.getenv('GITHUB_TOKEN', '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')

HEADERS = {'Authorization': f'token {GIT_TOKEN}'}