import flask
from flask import Flask, render_template, request, make_response, session, redirect, url_for
import content_manager
import models
import user_manager
import hashlib
import os


app = Flask(__name__)
USERS = []
CONTENT = []
LOGGED_USER = None
SECRET_KEY = '\x8c_}\xd7\x9a\xe0\t\x98K\x9a-\x9c\x94{\xc1\xbd4\xfd\x10\x9c\x13U\x8ai\xd1'


@app.before_request
def check_user_log():
    session.permanent = True
    global LOGGED_USER
    flask.g.user = None
    flask.g.users = user_manager.USERS
    flask.g.content = content_manager.CONTENT
    if 'user' in session:
        flask.g.user = user_manager.get_name_by_username(session.get('user'))


@app.route('/')
def index():
    return redirect(url_for('post_content'))


@app.route('/post', methods=['GET', 'POST'])
def post_content():
    if request.method == 'POST':
        author = request.form['author']
        if not author:
            author = "Ghost"
        if 'user' in session:
            author = user_manager.get_name_by_username(session.get('user'))
        text = request.form['text']
        pid = content_manager.post_content(author, text)
        return redirect('/post/' + pid)
    else:
        return render_template('post_form.html')


@app.route('/delete_post', methods=['DELETE'])
def delete_post():
    pid = request.headers['pid']
    content_manager.delete_post(pid)
    global CONTENT
    CONTENT = flask.g.content = content_manager.CONTENT
    return make_response()


@app.route('/post/<pid>')
def post(pid):
    if request.method == 'GET':
        post_object = None
        for content in CONTENT:
            if content.pid == pid:
                post_object = content
                break
        post_object.text = content_manager.get_content(pid)
        print(post_object.text)
        return render_template('post.html', post=post_object)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        username = request.form['username']
        password = get_password_hash(request.form['password'])
        if user_manager.signup_user(name, username, password):
            session['user'] = username
            session.modified = True
            return redirect(url_for('post_content'))
        return render_template('signup.html', erorr="username already taken")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = get_password_hash(request.form['password'])
        print(password)
        if user_manager.authenticate_user(username, password):
            session['user'] = username
            return redirect(url_for('post_content'))
        return render_template('login.html', erorr="username and password doesn't match!")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


def get_password_hash(password):
    hashed_password = hashlib.sha1(password.encode('utf-8'))
    return hashed_password.digest()


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    if not os.path.isdir('./data'):
        os.mkdir('./data')
    user_manager.initialize()
    content_manager.initialize()
    USERS = user_manager.USERS
    CONTENT = content_manager.CONTENT
    app.run(debug=True)

