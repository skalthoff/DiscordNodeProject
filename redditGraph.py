#from heapq import merge
import praw
import time
from py2neo import Graph, Node, Relationship
#import pandas as pd
#import numpy as np
#from py2neo.bulk import merge_nodes, merge_relationships

reddit = praw.Reddit(
            user_agent="bot name",
            client_id="EYwG-SMcl6cdbw",
            client_secret="CW1lJ0PkQPcsaKTx35FLEbQPboUFlQ",
            username="epic_gamer_4268",
            password=".e9Yy9i8A9-X$uh",
        )

#graph = Graph("bolt://3.239.191.198:7687", auth=("neo4j", "blanks-prisons-activities"))
graph = Graph("bolt://0.0.0.0:7687")

def getSubredditTop(subreddit):
    for submission in subreddit.top(limit=8):
        subReddit = Node("Subreddit", name=subreddit.display_name, RedditId=subreddit.id)
        submissionNode = Node("Submission", name=submission.title, subreddit=submission.subreddit.display_name, RedditId=submission.id)
        
        if submission.author is not None:
            author = reddit.redditor(submission.author.name)
            userNode = Node("User", name=author.name, RedditId=author.name)
            posting = Relationship(userNode, "POSTED", submissionNode)
            submitting = Relationship(submissionNode, "SUBMITTED_TO", subReddit)
            graph.merge(posting, "User", "name")
            graph.merge(submitting, "Submission", "RedditId")
            getUserTopSubmissions(author)
        else:
            author = "deleted"
            userNode = Node("User", author, author)
            graph.merge(Relationship(submissionNode, "Submitted to", subReddit), "Submission", "RedditId")

        
        
        
def getUserTopSubmissions(author):
    userSubreddits = []
    if author == "deleted":
        return
    try:
        for submission in author.submissions.top(limit=8):
                author = reddit.redditor(submission.author.name)
                submissionNode = Node("Submission", name=submission.title, subreddit=submission.subreddit.display_name, RedditId=submission.id)
                subReddit = Node("Subreddit", name=submission.subreddit.display_name, RedditId=submission.subreddit.id)
                userSubreddits.append(author.submissions.top(limit=8))
                userNode = Node("User", name=author.name, RedditId=author.id)
                graph.merge(Relationship(userNode, "Authored", submissionNode), "User", "name")
                graph.merge(Relationship(submissionNode, "Submitted to", subReddit), "Submission", "RedditId")
    except Exception as e:
        print(e)
        
        return userSubreddits
            



def recursiveSubredditGrabber(subreddit, depth):
    if depth == 0:
        return
    subreddit = reddit.subreddit(subreddit)
    getSubredditTop(subreddit)
    for submission in subreddit.top(limit=8):
        if submission.author is not None:
            author = reddit.redditor(submission.author.name)
            userSubreddits = getUserTopSubmissions(author)
    depth -= 1
    for subreddit in userSubreddits:
        recursiveSubredditGrabber(subreddit, depth)
    
    
def main():
    recursiveSubredditGrabber("Sino", 4)


if __name__ == "__main__":
    main()