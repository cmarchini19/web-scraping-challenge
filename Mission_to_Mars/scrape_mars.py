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


# Start scrape
def scrape():
    browser = init_browser

    ###NASA MARS NEWS
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Identify parent element data
    news_title_paragraph = news_soup.find('div', class_="list_text")

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

    ###MARS WEATHER
    # Establish Twitter link
    mars = {}
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    weather_soup = bs(html, 'html.parser')

    mars_weather_tweet = weather_soup.find_all('article')

    tweet_weather=[]
    for x in mars_weather_tweet:
        tweet = x.find("div",attrs={"data-testid":"tweet"})
    
        for j in tweet.find("div",class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"):
               tweet_weather.append(j.parent.text)
            
    tweet_weather[0]

    ###MARS FACTS
    browser = Browser('chrome', **executable_path, headless=False)

    #Establish URL
    mars_facts_url = 'https://space-facts.com/mars/'

    # Make table to scrape facts
    tables = pd.read_html(mars_facts_url)

    # Establish DataFrame Table
    facts_df = tables[0]
    facts_df.columns = ['Description', 'Values']

    # Generate HTML table from DataFrames
    facts_html_table = facts_df.to_html()

    # Strip unwanted lines to clean up table
    facts_html_table.replace('\n', '')

    # Final cleaned HTML table
    final_facts_html_table = facts_html_table.replace('\n', '')

    ###Mars Hemispheres
    #Cerberus Hemisphere URL Connection info
    cerberus_hemisphere = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(cerberus_hemisphere)

    html = browser.html
    cerb_hemi_soup = bs(html, 'html.parser')

    cerb = cerb_hemi_soup.body.find('img', class_= 'wide-image')
    cerb_img = cerb['src']

    cerb_img_url = f'https://astrogeology.usgs.gov'+ cerb['src']

    #Schiaparelli Hemisphere URL Connection info
    schia_hemisphere = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(schia_hemisphere)

    html = browser.html
    schia_hemi_soup = bs(html, 'html.parser')

    schia = schia_hemi_soup.body.find('img', class_= 'wide-image')
    schia_img = schia['src']

    schia_img_url = f'https://astrogeology.usgs.gov'+ schia['src']

    # Syrtis Major Hemisphere URL Connection info
    sm_hemisphere = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(sm_hemisphere)

    html = browser.html
    sm_hemi_soup = bs(html, 'html.parser')

    sm = sm_hemi_soup.body.find('img', class_= 'wide-image')
    sm_img = sm['src']

    sm_img_url = f'https://astrogeology.usgs.gov'+ sm['src']

    #Valles Marineris Hemisphere URL Connection info
    vm_hemisphere = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(vm_hemisphere)

    html = browser.html
    vm_hemi_soup = bs(html, 'html.parser')

    vm = vm_hemi_soup.body.find('img', class_= 'wide-image')
    vm_img = vm['src']

    vm_img_url = f'https://astrogeology.usgs.gov'+ vm['src']

    ###Consolidated list of each of Mars Hemisphere's Images
    # Create list of dictionaries of all hemisphere images

    mars_hemi_imgs =[
        {"title": "Cerberus Hemisphere", "img_url": cerb_img_url},
        {"title": "Schiaparelli Hemisphere", "img_url": schia_img_url},
        {"title": "Syrtis Major Hemisphere", "img_url": sm_img_url},
        {"title": "Valles Marineris Hemisphere", "img_url": vm_img_url},
        ]

    ###MARS DATA DICTIONARY
    mars = {}
    mars ["Mars Article Title"]=news_title
    mars ["Mars Article Paragraph"]=news_para
    mars ["Mars JPL Featured Image"]=featured_image_url
    mars ["Mars Twitter Weather"]=tweet_weather[0]
    mars ["Mars Facts"]=final_facts_html_table
    mars ["Mars Hemispheres"]=mars_hemi_imgs

    #Close the browser after scraping
    browser.quit()

    #Return my results
    return mars