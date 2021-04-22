from flask import Flask
from flask.templating import render_template
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:VIDgnh48123@node12713-project.app.ruk-com.cloud:11012") 
db = client["project"] 

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1',port = 3000)