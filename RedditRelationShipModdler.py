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

graph = Graph("bolt://0.0.0.0:7687")


def getSubmissionsinSubreddit(subreddit):
    try:
        for submission in subreddit.top(limit=200):
            subredditNode = Node("Subreddit", name=subreddit.display_name, RedditId=subreddit.id)
            submissionNode = Node("Submission", name=submission.title, subreddit=submission.subreddit.display_name, RedditId=submission.id)
            authorNode = Node("User", name=submission.author.name, RedditId=submission.author.name)
            graph.merge(Relationship(authorNode, "posted", submissionNode), "User", "name")
            graph.merge(Relationship(submissionNode, "submitted to", subredditNode), "Submission", "RedditId")
            getSubmissionsByUser(reddit.redditor(submission.author.name))
    except AttributeError:
        return
def getSubmissionsByUser(author):
    try:
        for submission in author.submissions.top(limit=20):
            submissionNode = Node("Submission", name=submission.title, subreddit=submission.subreddit.display_name, RedditId=submission.id)
            subredditNode = Node("Subreddit", name=submission.subreddit.display_name, RedditId=submission.subreddit.id)
            authorNode = Node("User", name=author.name, RedditId=author.id)
            graph.merge(Relationship(authorNode, "authored", submissionNode), "User", "name")
            graph.merge(Relationship(submissionNode, "submitted to", subredditNode), "Submission", "RedditId")
        #except 403:
    except Exception as e:
        print(e)
        return

def main():
    subreddit = reddit.subreddit("AskReddit")
    getSubmissionsinSubreddit(subreddit)
    
if __name__ == "__main__":
    main()