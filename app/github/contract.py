from app.github.beans import PullRequest, Repo, PullRequestComment, PullRequestState, InlineComment
from app.github import apis

def getDiffForPR(pullRequest: PullRequest) -> str:
    return apis.getPullRequestDiff(pullRequest.repo, pullRequest.prNumber)

def createPRComment(pullRequest: PullRequest, comment: PullRequestComment) -> PullRequestComment: 
    apis.createPRComment(pullRequest.repo, pullRequest.prNumber, comment.content)

def _getBeanFromPRDict(repo: Repo, prDict: dict) -> PullRequest:
    return PullRequest(
        repo=repo,
        prNumber=prDict.get('number'),
        title=prDict.get('title'),
        id=prDict.get('id'),
        state=PullRequestState[prDict.get('state').upper()],  
        headCommitSha=prDict['head']['sha']
    )

def _getBeanFromRepoDict(repoDict: dict) -> Repo:
    return Repo(owner=repoDict['owner']['login'], name=repoDict['name'])

def getPullRequestBeanFromDicts(repoDict: dict, prDict: dict) -> PullRequest:
    repoBean = _getBeanFromRepoDict(repoDict)
    return _getBeanFromPRDict(repoBean, prDict) 

def createInlineComment(pullRequest: PullRequest, inlineComment: InlineComment) -> dict: 
    return apis.createInlineComment(pullRequest=pullRequest, inlineComment=inlineComment)




