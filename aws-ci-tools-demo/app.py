from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my DevOps Journey"

@app.route('/about')
def about():
    return "Mustapha is a fast, curious learner with a can do attitude. In pursuit of being a cracked Engineer!"

@app.route('/DevOps')
def devops():
    return "DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the development lifecycle and deliver software faster."


if __name__ == '__main__':
    app.run(debug=True)