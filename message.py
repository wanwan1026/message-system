from math import nan
from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app = Flask(__name__,static_folder="static",static_url_path="/")
app.config['SECRET_KEY'] = 'ricetia' 

@app.route("/")
def index():
	return render_template("message.html")

app.run(port=3000)
# app.run(host="0.0.0.0",port=3000)