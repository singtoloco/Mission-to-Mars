from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()


    ### NASA Mars News ======= ###
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all('div', class_="list_text")

    news_title  = results[0].find('div', class_="content_title").text
    news_p  = results[0].find('div', class_="article_teaser_body").text


    ### JPL Mars Space Images - Featured Image ======= ###
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all('div', class_="carousel_container")

    for result in results:
        # Error handling
        try:
            
            featured_image_url  = result.find('article', class_="carousel_item")['style']  

            if (featured_image_url):
                
                featured_image_url = featured_image_url.split("('", 1)[1].split("')")[0]
                featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url                

        except AttributeError as e:
            print(e)


    ### Mars Weather ======= ###
    url = 'https://twitter.com/marswxreport?lang=en/'
    browser.visit(url)

    # html = browser.html
    # soup = BeautifulSoup(html, "html.parser")

    # results = soup.find_all('div', class_="content")

    # mars_weather = results[0].find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # sep = 'pic.twitter'
    # mars_weather = mars_weather.split(sep, 1)[0]
    # mars_weather = mars_weather.replace("\n", ", ")
    
    # <<<<<<<<<<<<<<<<<<  From solution
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")

    # First, find a tweet with the data-name `Mars Weather`
    tweet_attrs = {"class": "tweet", "data-name": "Mars Weather"}
    mars_weather_tweet = weather_soup.find("div", attrs=tweet_attrs)

    # Next, search within the tweet for the p tag containing the tweet text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    # From solution >>>>>>>>>>>>>>>>>>>>>>>>

    ### Mars Facts ======= ###
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df_table = tables[0]
    df_table.columns = ['Descripton', 'Value']
    df_table.set_index('Descripton', inplace=True)
    mars_facts = df_table.to_html()


    ### Mars Hemispheres  ======= ###
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all('div', class_='description')

    base_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []

    for result in results:
        
        image_dict = {}
    
        title = result.find('h3').text
        product_link = result.find('a')['href']
        product_link = base_url + product_link
    
        image_dict['title'] = title
        
        browser.visit(product_link)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, "html.parser")
        image_url = image_soup.find('img', class_='wide-image')['src']
        image_url = base_url + image_url
    
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

