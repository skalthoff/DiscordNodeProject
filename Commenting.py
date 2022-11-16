import praw
from py2neo import Graph, Node, Relationship



graph = Graph("bolt://192.168.1.11:7687")

reddit = praw.Reddit(client_id='PvOMYYBeEGY7wKYvLefm5A', client_secret="mSraEuCqh6YEGaAClL2vW19EHOgH3w", user_agent='user_agent')




def main():
    GraphedSubmissions = graph.run("MATCH (n:Submission) RETURN n LIMIT 1").data()
    for submission in GraphedSubmissions:
        submissionId = submission['n']['RedditId']
        submission = reddit.submission(id=submissionId)
        submission.comments.replace_more(limit=0)
        for commentNum, comment in enumerate(submission.comments.list()):
            if commentNum > 10:
                break
            commentNode = Node("Comment", RedditId=comment.id, name=comment.body, subreddit=submission.subreddit.display_name, submission=submission.title)
            if comment.author is not None:
                authorNode = Node("User", name=comment.author.name, RedditId=comment.author.name)
                graph.merge(Relationship(authorNode, "commented", commentNode), "ID", "RedditId")
            else:
                authorNode = Node("User", name="Deleted", RedditId="Deleted")
            submissionNode = Node("Submission", RedditId=submission.id, name=submission.title, subreddit=submission.subreddit.display_name)
            graph.merge(Relationship(authorNode, "commented", commentNode), "ID", "RedditId")
            graph.merge(Relationship(commentNode, "commented on", submissionNode), "ID", "RedditId")
    
main()