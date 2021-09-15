import json
import os
import models

USERS_JSON_PATH = './data/users.json'
USERS = []


def initialize():
    if not os.path.isfile(USERS_JSON_PATH):
        users_json = open(USERS_JSON_PATH, 'w+')
        users_json.write('[]')
    users_json = open(USERS_JSON_PATH, 'r')
    global USERS
    json_content = users_json.read()
    if not json_content:
        json_content = "[]"
    USERS = [models.User(**user_object) for user_object in json.loads(json_content)]


def save_data():
    users_file = open(USERS_JSON_PATH, 'w')
    users_file.write(get_serialized_users(USERS))
    users_file.close()


def authenticate_user(username, password):
    for user in USERS:
        if user.username == username and str(user.password) == str(password):
            return True
    return False


def get_serialized_users(users):
    users_json = "["
    user_encoder = models.UserEncoder()
    for user in users:
        users_json += json.dumps(user_encoder.encode(user)) + ", "
    users_json = users_json[0:len(users_json)-2]
    users_json += "]"
    return users_json


def get_name_by_username(username):
    for user in USERS:
        if user.username == username:
            return user.name
    return None


def signup_user(name, username, password):
    for user in USERS:
        if user.username == username:
            return False
    user = models.User(name, username, password)
    USERS.append(user)
    save_data()
    return True
