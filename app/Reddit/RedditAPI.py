import praw
import json
from datetime import datetime, timezone

from Reddit.Post import Post
from Reddit.PostList import PostList
from Reddit.Comment import Comment
from Reddit.CommentList import CommentList

class RedditAPI:

    __reddit : praw.Reddit

    def __init__(self, config_path: str):
        """
            Inizializza l'API di Reddit utilizzando le credenziali fornite in un file di configurazione JSON.
        PARAMETRI:
            config_path (str): Il percorso del file di configurazione JSON contenente le credenziali.
        """
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        self.__reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            username=config['username'],
            password=config['password'],
            user_agent=config['user_agent']
        )

    def get_posts(self, subreddit_name: str, want_comment=True, limit: int = 10) -> PostList:
        subreddit = self.__reddit.subreddit(subreddit_name)
        posts = subreddit.new(limit=limit)

        post_list = PostList()

        for post in posts:
            
            c = CommentList()
            if want_comment:
                for comment in post.comments.list():
                    if not isinstance(comment, praw.models.Comment):
                        continue
                
                    c.append(Comment(
                        comment.body,
                        datetime.fromtimestamp(comment.created_utc, tz=timezone.utc)
                    ))

            post_list.append(Post(
                post.title,
                post.selftext,
                datetime.fromtimestamp(post.created_utc, tz=timezone.utc),
                c
            ))

        return post_list

