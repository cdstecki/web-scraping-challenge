# Dependencies
import os
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import time
from splinter import Browser
import requests


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():    
    browser = init_browser()
    
    """
    NASA Mars News
    """

    # Navigate to News URL
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    time.sleep(4)
    
    news_html = browser.html
    soup = BeautifulSoup(news_html,'html.parser')

    # Retrieve the latest news title
    news_title = soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    """
    Mars Img
    """

    # Navigate to Featured Image URL
    space_image_url = 'https://spaceimages-mars.com/'
    browser.visit(space_image_url)
    time.sleep(4)
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    feature_image = soup.find(class_= 'headerimage fade-in')
    featured_image_url = space_image_url + feature_image['src']


    """
    Mars_data
    """

    # Navigate to Fact URL
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    time.sleep(4)
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Use Pandas to scrape table of facts
    tables = pd.read_html(requests.get('https://galaxyfacts-mars.com/').text)
    # tables = pd.read_html(facts_url)

    # Retrieve the table containing facts about Mars
    facts_df = tables[1]
    facts_df.columns =['Description', 'Value']
    idx_df = facts_df.set_index("Description")
    # Export to a HTML file
    mars_df = idx_df.to_html(border="1",justify="left")   

    # Convert the dataframe to a HTML table and save to html file
    facts_table = facts_df.to_html()
    facts_table.replace('\n','')

    """
    Mars Hemispheres
    """

    # Navigate to Hemisphere URL
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)
    time.sleep(4)
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Collect the urls for the hemisphere images
    items = soup.find_all("div", class_="item")

    main_url = 'https://marshemispheres.com/'
    hemisphere_image_urls = []
    for item in items:
        hemisphere_url = f"{main_url}{item.find('a', class_='itemLink')['href']}"
        
        # Navigate to the page
        browser.visit(hemisphere_url)
        hemisphere_html = browser.html
        soup = BeautifulSoup(hemisphere_html,'html.parser')
        
        img_url = soup.find('img', class_="wide-image")['src']
        title = soup.find('h2', class_="title").text
        
        hemisphere_image_urls.append({"title":title,"img_url":f"{main_url}{img_url}"})

    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_fact_table": facts_table, 
        "hemisphere_images": hemisphere_image_urls
    }
    browser.quit()

    return mars_info
