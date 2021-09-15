import json


class UserEncoder:
    def encode(self, user):
        return {
                "name": user.name,
                "username": user.username,
                "password": str(user.password)
                }


class PostEncoder:
    def encode(self, post):
        return {
                "pid": post.pid,
                "author": post.author,
                }


class User:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password


class Post:
    def __init__(self, pid, author):
        self.pid = pid
        self.author = author
        self.text = ""
