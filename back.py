from flask.helpers import url_for
import pymongo
import bcrypt
from flask import Flask,session,render_template,request,redirect
from flask.templating import render_template
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://admin:VIDgnh48123@node12713-project.app.ruk-com.cloud:11012") 
db = client["project"] 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    if 'email' in session:
        ses =  'You are logged in as ' + session['email']
    return render_template("menu.html" , ses = ses)

@app.route("/Register")
def Register():
    return render_template("Register.html")

########################################################################### LOGIN ###############################################################################################################
@app.route("/login")
def login():
    if 'email' in session:
        return 'You are logged in as ' + session['email']

    return render_template('Login.html')

@app.route('/loginBackend', methods=['POST'])
def loginBackend():
    users = db.customer
    login_user = users.find_one({'email': request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()):
            session['email'] = request.form['email']
            return redirect(url_for('menu'))

    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    char = db.customer
    if request.method == 'POST':
        users = char
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            emaila = request.form['email']
            users.insert_one({'username' : request.form['username'], 'password' : hashpass , 'email':emaila})
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        
        return render_template('index.html')

    return render_template('Register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

###############################################################################################################################################################################################


if __name__ == "__main__":
    app.run(host='127.0.0.1',port = 3000)