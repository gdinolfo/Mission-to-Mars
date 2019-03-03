#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests as req
import time
import pandas as pd

def scrape():
    executable_path = {'executable_path':'/temp/chromedriver'}
    browser = Browser('chrome', **executable_path)

    #visit site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #parsing html
    html_code = browser.html
    soup = BeautifulSoup(html_code, 'html.parser')

    #collect titles and paragraphs
    news_title = soup.find('div', class_='content_title').text
    paragraph = soup.find('div', class_='article_teaser_body').text

    browser.quit()

    # print(news_title)
    # print(paragraph)


    # # NASA JPL Mars Space Images - Featured Image

    # launch browser
    executable_path = {'executable_path':'/temp/chromedriver'}
    browser = Browser('chrome', **executable_path)
    # Visit the url for JPL Featured Space Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html_code = browser.html
    soup = BeautifulSoup(html_code, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    browser.click_link_by_partial_text('more info')

    #get image html code
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')

    image_path = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + image_path

    # print(featured_image_url)


    # # Mars Weather

    #getting weather on mars from twitter feed
    twitter_mars_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_mars_weather)
    weather_html = browser.html
    twitter_soup = BeautifulSoup(weather_html, 'html.parser')

    mars_twitter = twitter_soup.find_all('div', class_='js-tweet-text-container')

    browser.quit()

    mars_weather = mars_twitter[3].text
    # print(mars_weather[0].text)

    # # Mars Facts

    # read page
    facts_url = 'http://space-facts.com/mars/'
    read_mars_facts = pd.read_html(facts_url)
    #create dataframe
    mars_df = read_mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)

    # display df
    mars_df

    #convert to html string
    mars_html = mars_df.to_html()
    mars_html

    # Hemispheres

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_req = req.get(usgs_url)
    hemi_soup = BeautifulSoup(usgs_req.text, 'html.parser')
    hemi_list = hemi_soup.find_all('a', class_='itemLink product-item')

    hemisphere_image_urls = []
    for hemi_img in hemi_list:
        img_title = hemi_img.find('h3').get_text().replace('Enhanced', '')
        hemi_img_link = 'https://astrogeology.usgs.gov/' + hemi_img['href']
        img_soup = BeautifulSoup(req.get(hemi_img_link).text, 'html.parser')
        img_download = img_soup.find('div', {'class':'downloads'})
        img_url = img_download.find('a')['href']
        hemisphere_image_urls.append({'title': img_title, 'img_url': img_url})

    hemisphere_image_urls

    mars_dict = {
        "news_title": news_title,
        "paragraph": paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_html": mars_html,
        "hemisphere_images": hemisphere_image_urls
    }
    return mars_dict