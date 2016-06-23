from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    #return "Hello World!"
    return render_template('index.html')

@app.route("/<username>")
def home(username):
    return render_template('home.html',user=username)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
