from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class PullRequestState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"

@dataclass
class Repo:
    owner: str
    name: str

@dataclass 
class PullRequest: 
    repo: Repo 
    prNumber: int 
    title: str 
    id: str
    state: PullRequestState
    headCommitSha: str
    
class CommentProtocol(Protocol):
    content: str 
    repo: Repo 
    
@dataclass
class PullRequestComment(CommentProtocol):
    content: str 
    repo: Repo 

@dataclass 
class InlineComment(CommentProtocol): 
    content: str 
    repo: Repo 
    line: int 
    file: str 

