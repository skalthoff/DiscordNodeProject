import praw
import time
from py2neo import Graph, Node, Relationship
import pandas as pd
import numpy as np

reddit = praw.Reddit(
            user_agent="bot name",
            client_id="EYwG-SMcl6cdbw",
            client_secret="CW1lJ0PkQPcsaKTx35FLEbQPboUFlQ",
            username="epic_gamer_4268",
            password=".e9Yy9i8A9-X$uh",
        )

graph = Graph("bolt://3.239.191.198:7687",
    auth=("neo4j", "blanks-prisons-activities"))


def getSubredditTop(subreddit):
    
    
    subreddit = reddit.subreddit(subreddit)
    
    top = subreddit.top(limit=50)
    for submissionCount, submission in enumerate(top):
        SUBMISSION = Node("Submission", name=submission.title, subreddit=submission.subreddit.display_name)
        SUBREDDIT = Node("SubReddit", name=subreddit.display_name, redditId=subreddit.id)
        SUBMISSION = Node("Submission", name=submission.title, subreddit=submission.subreddit.display_name , redditId=submission.id)
        
        try:
            AUTHOR = Node("User", name=submission.author.name, redditId=submission.author.name)
        except AttributeError:
            AUTHOR = Node("User", name="deleted", redditId="deleted")
        SUBMITTED_TO = Relationship(SUBMISSION, "Submitted to", SUBREDDIT)
        graph.merge(SUBMITTED_TO, "Submission", "name")
        
        AUTHORED = Relationship(AUTHOR, "Authored", SUBMISSION)
        graph.merge(AUTHORED, "User", "name")
        print(f"Submssion #{submissionCount} Title: {submission.title}")
        if submission.author is not None:
            author = reddit.redditor(submission.author.name)
            print(author.name)
            getUserTopComments(author)
                
        
        
        
def getUserTopComments(user):
    try:
        top = user.submissions.top(limit=5)
        for submission in top:
            
            subreddit = submission.subreddit.display_name
            SUBMISSION = Node("Submission", name=submission.title, subreddit=submission.subreddit.display_name , redditId=submission.id)
            SUBREDDIT = Node("SubReddit", name=submission.subreddit.display_name, redditId=submission.subreddit.id)
            try:
                AUTHOR = Node("User", name=submission.author.name, redditId=submission.author.id)
            except AttributeError:
                AUTHOR = Node("User", name="deleted", redditId="deleted")
            SUBMITTED_TO = Relationship(SUBMISSION, "Submitted to", SUBREDDIT)
            graph.merge(SUBMITTED_TO, "Submission", "name")
            AUTHORED = Relationship(AUTHOR, "Authored", SUBMISSION)
            graph.merge(AUTHORED, "User", "name")
    except Exception as e:
        print(f"Error: {e}")
    

getSubredditTop("Sino")