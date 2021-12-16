from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Crate flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data_dict = mongo.db.mars_data_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_data_dict)


@app.route("/scrape")
def scrape():
    mars_data_dict = mongo.db.mars_data_dict
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert = True
    mars_data_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)