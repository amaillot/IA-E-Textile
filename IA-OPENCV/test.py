from __init__ import Flask
app = Flask(__name__)

@app.route("/")
def test():
    print('test retour python')