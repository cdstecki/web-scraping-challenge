# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():    
    
    # NASA Mars News
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    # Retrieve the latest news title
    news_title = soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Print the Latest title and its first paragraph
    print(news_title)
    print(f"------------------------------------------------")
    print(news_p)


    # JPL Mars Space Images - Featured Image
    space_image_url = 'https://spaceimages-mars.com/'
    browser.visit(space_image_url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    feature_img = soup.find(class_= 'headerimage fade-in')
    print(feature_img['src'])

    feature_image_url = space_image_url + feature_img['src']
    print(feature_image_url)


    # Mars Facts
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Use Pandas to scrape table of facts
    tables = pd.read_html(facts_url)
    tables

    # Use indexing to slice the table to a dataframe
    facts_df = tables[1]
    facts_df.columns =['Description', 'Value']
    facts_df

    # Convert the dataframe to a HTML table and save to html file
    facts_table = facts_df.to_html()
    facts_table.replace('\n','')
    print(facts_table)



    hemi_image_url = 'https://marshemispheres.com/'
    browser.visit(hemi_image_url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Collect the urls for the hemisphere images
    items = soup.find_all("div", class_="item")

    main_url = 'https://marshemispheres.com/'
    hemisphere_urls = []

    for item in items:
    hemisphere_urls.append(f"{main_url}{item.find('a', class_='itemLink')['href']}")

    print(*hemisphere_urls, sep = "\n") 

    # Create a list to store the data
    hemisphere_image_urls = []

    # Loop through each url
    for url in hemisphere_urls:
        # Navigate to the page
        browser.visit(url)
    
        # Assign the HTML content of the page to a variable
    
        hemisphere_html = browser.html
    
        # Parse HTML with Beautifulsoup
    
        soup = BeautifulSoup(hemisphere_html,'html.parser')
    
        img_url = soup.find('img', class_="wide-image")['src']
        title = soup.find('h2', class_="title").text
    
        hemisphere_image_urls.append({"title":title,"img_url":f"https://astrogeology.usgs.gov{img_url}"})

        mars_info = {
            "mars_news": {
                "news_title": news_title,
                "news_p": news_p,
                },
            "mars_img": featured_image_url,
            "mars_fact": mars_df,
            "mars_hemisphere": hemisphere_image_urls
        }
        browser.quit()

        return mars_info
