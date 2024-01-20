
#-----------------------------------
# Import 
#-----------------------------------
from flask import Flask,render_template,redirect,url_for,request, flash
from api.imageGenerator import generateImage
from flask_sqlalchemy import SQLAlchemy
import os
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
    # tickets = db.Column(db.Integer, default = 3)
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
            return render_template('login.html',message = "Incorrect Email or Password", type = 'error')
        return redirect(url_for('homepage',username = user.name,id = user.id))
            
    return render_template('login.html')

@app.route("/signup", methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["username"]
        password = request.form["password"]
        cnf = request.form["cnfpassword"]
        if not password == cnf:
            return render_template('signup.html', message = "Passwords Do Not Match!", type = "error")
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', message = "Email already registered!", type = "error")
        new_user = User(email=email, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        id = User.query.filter_by(email = email, password = password ).first().id

        return redirect(url_for('homepage', username = name, id = id))
    return render_template('signup.html')

@app.route("/profile/<username>,id=<id>")
def homepage(username,id = "guestid"):
    user = User.query.filter_by(name = username, id = id).first()
    if not user:
        return 'User {username} does not exist!!'
    countries = ['France', 'Greece', 'India', 'Japan', 'Russia']
    era = ['Ancient', 'Medieval', 'Renaissance', 'Futuristic', 'Contemporary', 'Modern']
    return render_template('profile.html', username = username, tickets = 10, countries = countries, eras = era)

@app.route('/exper')
def experienceSlide():
    return render_template('experience-slide.html')

@app.route("/experience", methods=["GET","POST"])
def experience():
    if request.method == "POST":
        era = request.form.get("selected_era")
        country = request.form.get("selected_country")
        image_folder = f'static\images\countries\{country}' 
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        for i, image_name in enumerate(image_files):
            image = generateImage(country, era, image_name)
            image.save(f"static/Images/Generated/{i}.jpg")
    
    return render_template('experience_slide.html')

#-----------------------------------
# Running the app
#-----------------------------------
if __name__ == '__main__':
    app.run(debug=True,port=5001)