#set dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Initialize my app
app = Flask(__name__)


#Set-up my connection to mongo
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

#Establish my routes

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data2 = scrape_mars.scrape()
    mongo.db.mars.update({}, mars_data2, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(port=5001)

