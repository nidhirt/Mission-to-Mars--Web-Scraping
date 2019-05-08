
#import dependencies
from bs4 import BeautifulSoup 
from splinter import Browser
import os
import pandas as pd
import time



def init_browser():
    #Site Navigation
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)
    #exec_path = {'executable_path': '/app/chromedriver/bin/chromedriver'}
    exec_path = {'executable_path': '/usr/local/bin/chromedriver' }
    return Browser('chrome', headless=True, **exec_path)



# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# MARS NEWS

def scrape_mars_news():
    try:
        browser = init_browser() #initiatize browser

        url = "https://mars.nasa.gov/news/"
        browser.visit(url)   #Visit NASA News url

        html=browser.html   #HTML Object
        soup = BeautifulSoup(html, "html.parser")  #Parse HTML with Beautiful soup


        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:
        browser.quit()

# MARS IMAGE

def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        image = soup.find("img", class_="thumb")["src"]
        featured_image_url = "https://www.jpl.nasa.gov" + image
        
         # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 

        return mars_info
    
    finally:
        browser.quit()


#MARS WEATHER

def scrape_mars_weather():

    try:
        # Initialize browser 
        browser = init_browser()

        #get mars weather's latest tweet from the website
        url_weather = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url_weather)
        html_weather = browser.html
        soup = BeautifulSoup(html_weather, "html.parser")
        mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        mars_info["mars_weather"] = mars_weather

        return mars_info

    finally:
        browser.quit()


# MARS FACTS

def scrape_mars_facts():

    try:

         # Initialize browser 
        browser = init_browser()

        facts_url = 'http://space-facts.com/mars/'
        mars_facts = pd.read_html(facts_url)

        mars_df = mars_facts[0]
        mars_df.columns = ['Description','Value']
        mars_df.set_index(['Description'])

        # Save html code to folder Assets
        data = mars_df.to_html()

        # Dictionary entry from MARS FACTS
        mars_info['mars_facts'] = data

        return mars_info

    finally:
        browser.quit() 


def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []
        
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
           
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu

        
        # Return mars_data dictionary 

        return mars_info

    finally:

        browser.quit()














