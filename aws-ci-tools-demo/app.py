from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my DevOps Journey"

@app.route('/about')
def about():
    return "Mustapha is a fast, curious learner with a can do attitude. In pursuit of being a cracked Engineer!"

if __name__ == '__main__':
    app.run(debug=True)     
