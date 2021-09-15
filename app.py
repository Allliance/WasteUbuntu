from flask import Flask, render_template, request, make_response
import user_manager

print("hello guys")
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('post_form.html')


@app.route('/post', methods=['POST', 'GET'])
def post():
    return render_template('post.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


if __name__ == "__main__":
    user_manager.initialize()
    app.run(debug=True)

