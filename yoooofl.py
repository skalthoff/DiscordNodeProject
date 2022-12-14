## Imports ##
import praw
from py2neo import Graph, Node, Relationship




reddit = praw.Reddit(
            user_agent="bot name",
            client_id="EYwG-SMcl6cdbw",
            client_secret="CW1lJ0PkQPcsaKTx35FLEbQPboUFlQ",
            username="epic_gamer_4268",
            password=".e9Yy9i8A9-X$uh",
        )

graph = Graph("bolt://192.168.1.11:7687")

def getSubmissionsinSubreddit(subreddit, depth):
    if (subreddit in subredditList):
        subredditList.remove(subreddit)
        subreddit = reddit.subreddit(subreddit)
    elif  len(subredditList) == 0:
        exit()
    
    try:
        if subreddit.display_name == "Home":
            return
        for submission in subreddit.top(limit=10):
            subredditNode = Node("Subreddit", RedditId=subreddit.id, name=subreddit.display_name, )
            submissionNode = Node("Submission", RedditId=submission.id, name=submission.title, subreddit=submission.subreddit.display_name, )
            authorNode = Node("User", name=submission.author.name, RedditId=submission.author.name)
            graph.merge(Relationship(authorNode, "posted", submissionNode), "ID", "RedditId")
            graph.merge(Relationship(submissionNode, "submitted to", subredditNode), "ID", "RedditId")
            getSubmissionsByUser(reddit.redditor(submission.author.name), depth)
    except AttributeError:
        return
def getSubmissionsByUser(author, depth):
    if depth == 0:
        return
    try:
        for submission in author.submissions.top(limit=10):
            submissionNode = Node("Submission", RedditId=submission.id, name=submission.title, subreddit=submission.subreddit.display_name)
            subredditNode = Node("Subreddit", RedditId=submission.subreddit.id, name=submission.subreddit.display_name)
            if submission.subreddit.display_name == "Home":
                return
            authorNode = Node("User",RedditId=author.id, name=author.name)
            graph.merge(Relationship(authorNode, "authored", submissionNode), "ID", "RedditId")
            graph.merge(Relationship(submissionNode, "submitted to", subredditNode), "ID", "RedditId")
            
            getSubmissionsinSubreddit(reddit.subreddit(submission.subreddit.display_name), depth-1)
        #except 403:
    except Exception as e:
        print(e)
        return
    


def main():
    global subredditList
    subreddits = reddit.subreddits.popular(limit=30)
    subredditList = [s.display_name for s in subreddits]
    for subreddit in subredditList:
        getSubmissionsinSubreddit(subreddit, depth=10)
    
    
if __name__ == "__main__":
    main()