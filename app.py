from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect,url_for
import scrape_mars

app = Flask(__name__)
# use Flask PyMongo to sync to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#index route
@app.route("/")
def index():
    # the info from database
    marsData = mongo.db.marsDB.find_one()
    
    return render_template("index.html", marsDB=marsData)
    
#scrape route
@app.route("/scrape")
def scrape():
    marsData=scrape_mars.scrape_all()
    print(marsData)
    # to a database
    marsData = mongo.db.marsDB
   
    # drop the table if exists 
    mongo.db.marsDB.drop()

    # scrape the mars
    data = scrape_mars.scrape_all()

    # load the dictionary to the MongoDB
    marsData.insert_one(marsData)
    marsData.update_one({}, {"$set": data}, upsert=True)
    # back to the index
    return redirect("/")

if __name__ == "__main__":
    app.run()