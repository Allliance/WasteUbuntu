import json

users = []

def initialize():
    users_json = open('data/users.json', 'r')
    users = json.loads(users_json.read())


class UserManager:
    def register_user(self):
        return 0
