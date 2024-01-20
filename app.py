
#-----------------------------------
# Import 
#-----------------------------------

from flask import Flask,render_template,redirect,url_for,request, flash
from api.imageGenerator import generateImage
from api.uploadImage import upload_to_imgbb
from flask_sqlalchemy import SQLAlchemy
import stripe
import time
import random
import json
import os

def read_json_file():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"era": "", "country": ""}
    return data

def write_json_file(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

#-----------------------------------
# Initialization 
#-----------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = "KCQIRRT#@#@"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/postgres'
YOUR_DOMAIN = 'http://localhost:4242'

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
        if User.query.filter_by(email= email).first():
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
    cntimg = ['https://images.pexels.com/photos/1694359/pexels-photo-1694359.jpeg',
              'https://images.pexels.com/photos/161275/santorini-travel-holidays-vacation-161275.jpeg',
              'https://images.pexels.com/photos/1007426/pexels-photo-1007426.jpeg',
              'https://images.pexels.com/photos/590478/pexels-photo-590478.jpeg',
              'https://images.pexels.com/photos/236294/pexels-photo-236294.jpeg']
    era = ['Ancient', 'Medieval', 'Renaissance', 'Futuristic', 'Contemporary', 'Modern']
    
    history_data = read_json_file()

    return render_template('profile.html', username = username, tickets = 10, countries = countries, eras = era, locs = cntimg, history_data = history_data)

@app.route("/experiences", methods=["GET","POST"])
def experiences():
    country = None
    era = None
    # url_list = []
    
    if request.method == "POST":
        era = request.form.get("selected_era")
        country = request.form.get("selected_country")
        image_folder = f'static/images/countries/{country}'  # Update with the path to your image folder
        if os.path.exists(image_folder):
            print("PATH DOESNT EXIST")
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        for i, image_name in enumerate(image_files):
            image = generateImage(country, era, image_name)
            image.save(f"static/images/Generated/{i}.jpg")
            # imgbb_url = upload_to_imgbb(f"static/images/Generated/{i}.jpg")
            # url_list.append(imgbb_url)
    
    return render_template('experience-slide.html', area=country, era=era)



@app.route("/experience", methods=["GET","POST"])
def experience():
    country = None
    era = None
    
    if request.method == "POST":
        era = request.form.get("selected_era")
        country = request.form.get("selected_country")
        images = [random.randint(0, 47) for _ in range(6)]
        time.sleep(20)    
        data = read_json_file()

        # Update data with new values
        data["era"] = era
        data["country"] = country

        # Write updated data back to JSON file
        write_json_file(data)
    
    return render_template('experience-slide.html', area=country, era=era, imagelist = images)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


#-----------------------------------
# Running the app
#-----------------------------------
if __name__ == '__main__':
    app.run(debug=True,port=5001)