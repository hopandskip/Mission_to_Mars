# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests

# Choose the executable path to driver 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

mars_info={}

#Grab the news from Nasa
def nasa_news_scrape():
    #initialize browser
    browser = init_browser()
    # Visit Nasa news page through splinter module
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)  
    #Use beautiful soup to look at the html page
    html = browser.html
    soup = bs(html, 'html.parser')
    # Retrieve the title and summary paragraph for the latest article (it comes up first)
    news_title = soup.find(class_='content_title').text
    news_p = soup.find(class_ = 'article_teaser_body').text

    mars_info["title"]=news_title
    mars_info["content"]=news_p

    return mars_info

# Grab the featured image from JPL
def featured_image_scrape():
    #initialize browser
    browser = init_browser()
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    #Use beautiful soup to look at the html page
    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    #Get the url of the image
    scraped_image_url = soup.find('article')['style']
    clean_image_url = scraped_image_url.replace("background-image: url('", "").replace("');","")
    featured_image_url = "https://www.jpl.nasa.gov/" + clean_image_url

    mars_info['featured_image']=featured_image_url

    return mars_info

# Get the latest weather updates of Mars from Mars Weather on Twitter
def weather_updates_scrape():
    #initialize browser   
    browser = init_browser()

    # Vist the Mars Weather twitter page and grab the latest weather
    mars_weather_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_twitter_url) 

    #Use beautiful soup to look at the twitter html page
    mars_weather_twitter_html = browser.html
    soup = bs(mars_weather_twitter_html, 'html.parser')

    # Get the tweet data
    mars_weather = soup.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_info['weather_info']=mars_weather

    return mars_info

# Grab facts about Mars from SpaceFacts
def mars_facts_scrape():
    #initialize browser
    browser = init_browser()

    # Vist the Mars Space Facts page and grab the facts about Mars
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url , encoding= "utf-8") 

    # Put the facts into a pandas table and rename the columns
    facts_df = tables[0]
    facts_df.columns = ['Description', 'Value']

    facts_df.set_index('Description', inplace=True)

    # Import the dataframe to an html
    mars_facts_html_table = facts_df.to_html()     

    # Save dataframe as an html file
    facts_df.to_html('mars_facts_table.html')  

    mars_info['mars_facts']=mars_facts_html_table
    
    return mars_info

# Mars Hemisphere Images
def mars_hemisphere_images_scrape():
    #initialize browser
    browser = init_browser()

    # Vist the USGS Astrogeology page and grab images of Mars
    mars_images_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_images_url)

    #Use beautiful soup to look at the html page
    mars_images_url_html = browser.html
    soup = bs(mars_images_url_html, 'html.parser')

    # return the links from the html page
    image_descriptions = soup.find_all('div',class_='description')

    hemisphere_image_urls=[]
    hemi_main_url = 'https://astrogeology.usgs.gov'

    # loop through each of the images and get the full size image
    for i in image_descriptions:
        # grab the title
        title = i.find('h3').text
        # grab the image link
        hemi_image_url = i.find('a', class_='itemLink product-item')['href']
        full_url = hemi_main_url + hemi_image_url
        # Go to the image link 
        browser.visit(full_url)
        # After going to the image url, find the full size image in the html
        hemi_images_html = browser.html
        soup = bs(hemi_images_html, 'html.parser')
        full_hemi_images_url = soup.find('img', class_='wide-image')['src']
        full_size_images_url = hemi_main_url + full_hemi_images_url
        # Append the title and url links to hemisphere_image_urls as a dictionary
        hemisphere_image_urls.append({'title':title, 'img_url': full_size_images_url})

    mars_info['hemisphere_images']=hemisphere_image_urls

    return mars_info