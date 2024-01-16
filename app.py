
#-----------------------------------
# import 
#-----------------------------------
from flask import Flask

app = Flask(__name__)

@app.route("/")
def landing():
    return "This is  a basic app"




#-----------------------------------
# running the app
#-----------------------------------
if __name__ == '__main__':
    app.run(debug=True,port=5340,host='0.0.0.0')