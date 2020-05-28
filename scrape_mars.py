import requests
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import splinter
import GetOldTweets3 as got


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def Scrape():
    executable_path={'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #dictionary for the scraped items
    mars_dict = {}

    # URL for news page
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    html = browser.html
    browser.visit(news_url)
    #scrape for the latest title and news paragraph text
    news_title = browser.find_by_css('div[class = "content_title"]').text
    news_title

    soup = BeautifulSoup(html, 'html.parser')
    #selects first list item that contains paragraph title and text
    p_text = soup.select_one('ul.item_list li.slide')
    news_title = p_text.find('div', class_ = 'content_title').text

    
    #finding text within the first list item(li)
    news_p = p_text.text



    #add to the dictionary
    mars_dict['News Title'] = news_title
    mars_dict['News Paragraph'] = news_p
    
    
    #browser session 
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    #Url for jpg page
    space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #browser
    browser.visit(space_images_url)
    #Use beautiful soup to find instance of images
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('div', class_ = 'img')

    #use Beautiful Soup to find img url
    for x in images:
        image = x.find('img')
        title = image['title']
        img_url = image['src']
        print('-----------')
        print(title)
        featured_image_url = 'https://www.jpl.nasa.gov' + img_url
        if title == 'Arsia Mons Summit':
            break
    
    #adding image url to dictionary
    mars_dict['Image url'] = featured_image_url

    #Mars Twitter Account
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(twitter_url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    #Scraping for the latest Mars weather tweet
    tweetCriteria = got.manager.TweetCriteria().setUsername("MarsWxReport")\
                                           .setTopTweets(True)\
                                           .setMaxTweets(10)
    mars_weather = got.manager.TweetManager.getTweets(tweetCriteria)[0]
    #adding tweet to dictionary
    mars_dict['Mars Weather'] = mars_weather
    #Mars Facts url
    facts_url = "https://space-facts.com/mars/"
    #make tables variable
    tables = pd.read_html(facts_url)
    
    #convert table to dataframe
    df = tables[0]
    df.columns = ['Titles', 'Stats']
    

    #turn table to html text
    html_table = df.to_html()
    mars_dict['HTML Table'] = html_table

    #end session
    browser.quit()

    return mars_dict

