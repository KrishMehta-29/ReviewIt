import app.github.auth as github_auth
import requests
from app.github.beans import Repo, PullRequest, InlineComment
from typing import Any, List, Dict

GITHUB_API_URL = "https://api.github.com"

def getAllPullRequests(repo: Repo) -> List[Dict[str, Any]]:
    headers = github_auth.getHeadersForRequest()

    url = f"{GITHUB_API_URL}/repos/{repo.owner}/{repo.name}/pulls?state=open"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

def getPullRequestDiff(repo: Repo, prNumber: int) -> str:
    headers = github_auth.getHeadersForRequest(getDiff=True) # Forces PR to return a diff

    url = f"{GITHUB_API_URL}/repos/{repo.owner}/{repo.name}/pulls/{prNumber}.diff"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.text

def getPullRequest(repo: Repo, prNumber: int) -> dict:
    headers = github_auth.getHeadersForRequest()

    url = f"{GITHUB_API_URL}/repos/{repo.owner}/{repo.name}/pulls/{prNumber}.diff"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

def createPRComment(repo: Repo, prNumber: int, comment: str) -> dict:
    headers = github_auth.getHeadersForRequest()
    url = f"{GITHUB_API_URL}/repos/{repo.owner}/{repo.name}/issues/{prNumber}/comments"
    response = requests.post(url, headers=headers, json={"body": comment})
    response.raise_for_status()
    
    return response.json()

def createInlineComment(pullRequest: PullRequest, inlineComment: InlineComment) -> dict: 
    headers = github_auth.getHeadersForRequest()

    # Create an inline comment
    url = f"{GITHUB_API_URL}/repos/{pullRequest.repo.owner}/{pullRequest.repo.name}/pulls/{pullRequest.prNumber}/comments"
    payload = {
        "body": inlineComment.content,
        "commit_id": pullRequest.headCommitSha,
        "path": inlineComment.file,
        "position": inlineComment.line,  # Use position instead of line
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()