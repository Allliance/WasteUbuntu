from flask import Flask, render_template, request, make_response

print("hello guys")
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST', 'GET'])
def post():
    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True)
