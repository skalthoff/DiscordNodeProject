## Imports ##
import time
from types import NoneType
import praw
from py2neo import Graph, Node, Relationship



reddit = [Reddit Api]

graph = Graph([IP Address])


def getSubmissionsinSubreddit(subreddit, depth):
    if depth < 0:
        return
        #start = time.perf_counter()
        #startNodes = len(graph.nodes)
        #
        # startRelationships = len(graph.relationships)
    
    if subreddit.display_name == "Home":
        return
    for submission in subreddit.top(limit=200):
        
        
        #print(f"Submission {subNum} in {subreddit.display_name}, at depth {depth}")
        subredditNode = Node("Subreddit", RedditId=subreddit.id, name=subreddit.display_name, )
        submissionNode = Node("Submission", RedditId=submission.id, name=submission.title, subreddit=submission.subreddit.display_name, )
        if (submission.author is None):
            authorNode = Node("User",RedditId="Deleted", name="Deleted")
            graph.merge(Relationship(submissionNode, "submitted to", subredditNode), "ID", "RedditId")
            
            
        else:
            authorNode = Node("User",RedditId=submission.author.name, name=submission.author.name)
            graph.merge(Relationship(authorNode, "posted", submissionNode), "ID", "RedditId")
            graph.merge(Relationship(submissionNode, "submitted to", subredditNode), "ID", "RedditId")
            getSubmissionsByUser(author=reddit.redditor(submission.author.name), depth=depth)
        #print(f"Added nodes: {len(graph.nodes) - startNodes}")
        #except nonetype:
    return
                
        
            
def getSubmissionsByUser(author, depth):
    if depth < 0:
        return
    try:
        for submission in author.submissions.top(limit=200):
            submissionNode = Node("Submission", RedditId=submission.id, name=submission.title, subreddit=submission.subreddit.display_name)
            subredditNode = Node("Subreddit", RedditId=submission.subreddit.id, name=submission.subreddit.display_name)
            if submission.subreddit.display_name == "Home":
                return
            if submission.author is not None:
                authorNode = Node("User",RedditId=author.id, name=author.name)
                graph.merge(Relationship(submissionNode, "submitted to", subredditNode), "ID", "RedditId")
            else:
                authorNode = Node("User",RedditId="Deleted", name="Deleted")
            graph.merge(Relationship(authorNode, "posted", submissionNode), "ID", "RedditId")
            getSubmissionsinSubreddit(reddit.subreddit(submission.subreddit.display_name), depth=depth-1)
    except Exception as e:
        print(e)
        return
    return
    #except 403:
        
    


def main():
    #subredditList = reddit.subreddits.popular(limit=10)
    subredditList = [reddit.subreddit("Sino")]
    for subreddit in subredditList:
        getSubmissionsinSubreddit(subreddit, depth=10)
    
    
if __name__ == "__main__":
    main()