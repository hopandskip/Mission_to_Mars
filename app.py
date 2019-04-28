from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    # Find data
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.nasa_news_scrape()
    mars_data = scrape_mars.featured_image_scrape()
    mars_data = scrape_mars.weather_updates_scrape()
    mars_data = scrape_mars.mars_facts_scrape()
    mars_data = scrape_mars.mars_hemisphere_images_scrape()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
