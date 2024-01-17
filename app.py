
#-----------------------------------
# Import 
#-----------------------------------
from flask import Flask,render_template,redirect,url_for,request

from flask_sqlalchemy import SQLAlchemy

#-----------------------------------
# Initialization 
#-----------------------------------
DATA_BASE = "database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DATA_BASE}'

app.config['SECRET_KEY'] = "KCQIRRT#@#@"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    name = db.Column(db.String(50),default = "Guest" )
with app.app_context():
    db.create_all()

#-----------------------------------
# Routes 
#-----------------------------------

@app.route("/")
def landing():
    return render_template('root.html')

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email = email, password = password ).first()
        if not user:
            return render_template('login.html',message = "Incorrect Email or PassWord", type = 'error')
        return redirect(url_for('homepage',username = user.name))
            
    return render_template('login.html')

@app.route("/signup", methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', message = "Account Is Already Created, Please Log In", type = 'error')
        name = request.form["username"]
        password = request.form["password"]
        cnf = request.form["cnfpassword"]
        if not password == cnf:
            return render_template('signup.html', message = "Passwords Do Not Match!", type = "error")
        new_user = User(email=email, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('homepage', username = name))
    return render_template('signup.html')

@app.route("/profile/<username>")
def homepage(username):
    return f'Username = {username}'
#-----------------------------------
# Running the app
#-----------------------------------
if __name__ == '__main__':
    app.run(debug=True,port=5340,host='0.0.0.0')