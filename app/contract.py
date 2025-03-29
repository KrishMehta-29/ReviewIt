# Main Contract 
from app.github.beans import PullRequest, Repo, PullRequestComment, PullRequestState
from app.github import contract as github_contract
from app.agents.agent import getAgentPRCommentsForDiff
from app.agents.inlineAgent import getAgentInlinePRCommentsForDiff

def getPullRequestFromWebhook(webhookJson) -> PullRequest: 
    repoDict = webhookJson['repository']   
    prDict = webhookJson['pull_request']

    return github_contract.getPullRequestBeanFromDicts(repoDict=repoDict, prDict=prDict)

def shouldAddCommentsToPullRequest(webhookJson: dict) -> bool: 
    if webhookJson['action'] != 'review_requested': 
        return False 
    
    if webhookJson['requested_reviewer']['login'] != "Review-It-Bot":
        return False 
    
    return True 

def handleWebhook(payload) -> bool:
    # Returns if the request was handled or ignored
    if shouldAddCommentsToPullRequest(payload):

        pullRequest = getPullRequestFromWebhook(payload)
        diff = github_contract.getDiffForPR(pullRequest)

        # prComment = getAgentPRCommentsForDiff(diff=diff)
        # comment = PullRequestComment(content=prComment)
        # github_contract.createPRComment(pullRequest, comment)

        commentsToCreate = getAgentInlinePRCommentsForDiff(diff)
        for comment in commentsToCreate:
            github_contract.createInlineComment(pullRequest=pullRequest, inlineComment=comment)

        return True 
    
    return False 
            

