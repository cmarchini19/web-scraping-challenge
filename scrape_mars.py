# Import dependencies we may need
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import time

# Initiate chromedrive information
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser

    ###NASA MARS NEWS
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Identify parent element data
    news_title_paragraph = news_soup.find('div', class_="list_text")
    # print(news_title_paragraph)

    # Identify title and print
    news_title = news_title_paragraph.find('div', class_="content_title").text

    # Identify paragraph and print
    news_para = news_title_paragraph.find('div', class_="article_teaser_body").text

    ###JPL MARS SPACE IMAGES - FEATURED IMAGE
    browser = Browser('chrome', **executable_path, headless=False)

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    browser.find_by_tag('footer').click()
    browser.find_by_text('more info     ').click()

    # Get/print featured image url information
    html = browser.html
    jpl_soup = bs(html, 'html.parser')

    featured_image_info = jpl_soup.find('figure', class_="lede").a.img

    # Create Featured Image URL
    featured_image_url = f'https://www.jpl.nasa.gov' + featured_image_info["src"]









if __name__ == '__main__':
    scrape()