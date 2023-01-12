# Imports
import praw
from py2neo import Graph, Node, Relationship

# Reddit API
reddit = [Reddit Api]

# Neo4j Graph
graph = Graph([IP Address])


def get_submissions_in_subreddit(subreddit, depth):
    if depth < 0:
        return

    if subreddit.display_name == "Home":
        return

    # Get top submissions in subreddit
    for submission in subreddit.top(limit=200):
        # Create subreddit and submission nodes
        subreddit_node = Node("Subreddit", RedditId=subreddit.id, name=subreddit.display_name)
        submission_node = Node("Submission", RedditId=submission.id, name=submission.title, subreddit=submission.subreddit.display_name)

        if submission.author is None:
            # Create user node for deleted account
            author_node = Node("User", RedditId="Deleted", name="Deleted")

            # Merge subreddit and submission nodes
            graph.merge(Relationship(submission_node, "submitted to", subreddit_node), "ID", "RedditId")

        else:
            # Create user node
            author_node = Node("User", RedditId=submission.author.name, name=submission.author.name)

            # Merge user, submission, and subreddit nodes
            graph.merge(Relationship(author_node, "posted", submission_node), "ID", "RedditId")
            graph.merge(Relationship(submission_node, "submitted to", subreddit_node), "ID", "RedditId")

            # Recursively get submissions by user
            get_submissions_by_user(author=reddit.redditor(submission.author.name), depth=depth)


def get_submissions_by_user(author, depth):
    if depth < 0:
        return

    try:
        # Get top submissions by user
        for submission in author.submissions.top(limit=200):
            # Create submission and subreddit nodes
            submission_node = Node("Submission", RedditId=submission.id, name=submission.title, subreddit=submission.subreddit.display_name)
            subreddit_node = Node("Subreddit", RedditId=submission.subreddit.id, name=submission.subreddit.display_name)

            if submission.subreddit.display_name == "Home":
                return

            if submission.author is not None:
                # Create user node
                author_node = Node("User", RedditId=author.id, name=author.name)

                # Merge submission and subreddit nodes
                graph.merge(Relationship(submission_node, "submitted to", subreddit_node), "ID", "RedditId")

            else:
                # Create user node for deleted account
                author_node = Node("User", RedditId="Deleted", name="Deleted")

            # Merge user and submission nodes
            graph.merge(Relationship(author_node, "posted", submission_node), "ID", "RedditId")

            # Recursively get submissions in subreddit
            get_submissions_in_subreddit(reddit.subreddit(submission.subreddit.display