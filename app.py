from flask import Flask, render_template

print("hello guys")
app = Flask(__name__)

@app.route('/')
def indexd():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)