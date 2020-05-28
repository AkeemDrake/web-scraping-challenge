from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def home():
    mars_dict = mongo.db.mars_dict.find()
    return render_template("index.html", mars_dict=mars_dict)
@app.route('/scrape')
def scrape():

    #find scraping command in from scrape_mars.py
    mars_dict = scrape_mars.Scrape()

    #add information to the dictionary
    post = {
        'news_title': mars_dict['news_title'],
        'news_para': mars_dict['news_p'],
        'featured_image_url': mars_dict['featured_image_url'],
        'mars_weather' : mars_dict['mars_weather'],
        'html_table' : mars_dict['html_table']
        }

 # Delete previous content
    mongo.db.mars_info.drop()
     # Insert new Mars info
    mongo.db.mars_info.insert_one(post)
    # Redirect back to home page
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)