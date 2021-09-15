import json
import os
import models
import hashlib
import time

CONTENT_JSON_PATH = './data/content.json'
CONTENT_DIRECTORY_PATH = './data/files'
CONTENT = []


def initialize():
    if not os.path.isfile(CONTENT_JSON_PATH):
        content_json = open(CONTENT_JSON_PATH, 'w+')
        content_json.write('[]')
    content_json = open(CONTENT_JSON_PATH, 'r')
    global CONTENT
    json_content = content_json.read()
    if not json_content:
        json_content = "[]"
    CONTENT = [models.Post(**content_object) for content_object in json.loads(json_content)]


def save_data():
    content_file = open(CONTENT_JSON_PATH, 'w')
    content_file.write(get_serialized_content(CONTENT))
    content_file.close()


def get_serialized_content(posts):
    posts_json = "["
    post_encoder = models.PostEncoder()
    for post in posts:
        posts_json += json.dumps(post_encoder.encode(post)) + ", "
    posts_json = posts_json[:len(posts_json)-2]
    posts_json += "]"
    return posts_json


def post_content(author, text):
    if not os.path.isdir(CONTENT_DIRECTORY_PATH):
        os.mkdir(CONTENT_DIRECTORY_PATH)
    hashcode = hashlib.sha1(str(time.time()).encode('utf-8'))
    post = models.Post(hashcode.hexdigest()[:8], author)
    post_file = open(os.path.join(CONTENT_DIRECTORY_PATH, post.pid), 'w+')
    post_file.write(text)
    post_file.close()
    CONTENT.append(post)
    save_data()
    return post.pid


def get_content(pid):
    post_file = open(os.path.join(CONTENT_DIRECTORY_PATH, pid), 'r')
    return post_file.read()
