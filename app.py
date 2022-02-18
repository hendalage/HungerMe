from flask import Flask

app = Flask("hunger_me")


@app.route("/")
def default():
    print("This is default route")