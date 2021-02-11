from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    
    html = browser.html
    soup = bs(html, "html.parser")

    articles = soup.find('ul', class_='item_list')

    title_list = []
    text_list = []


    for article in articles:
        title = article.find('div', class_='content_title')
        title = title.text.strip()
        text = article.find('div', class_='article_teaser_body')
        text = text.text.strip()
        title_list.append(title)
        text_list.append(text)


    latest_title = title_list[0]
    latest_text = text_list[0]

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('img', class_='headerimage fade-in')['src']
    parsed_url = url.split('/')
    featured_image_url = parsed_url[0]+'//'+ parsed_url[1] + '/' + parsed_url[2] + '/' + image
    
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_='collapsible results')

    links = results.find_all('div',class_='item')  
    hemisphere_image_urls = []

    for link in links:
        
        href = link.find('a')['href']
        
        url = "https://astrogeology.usgs.gov" + href
        browser.visit(url)
        enhanced_page = browser.html
        enhanced_page = bs(enhanced_page, 'html.parser')
        content = enhanced_page.find('section',class_='block metadata')
        title = content.find('h2',class_='title')
        title = title.text.strip()
        source = enhanced_page.find('li')
        img_url = source.find('a')['href']
        astro_dict = {'title':title,'img_url':img_url}
        hemisphere_image_urls.append(astro_dict)


    mars_data = {
        "hemishere_images":hemisphere_image_urls,
        "table": html_table,
        "featured_image":featured_image_url,
        "latest_title": latest_title,
        "latest_text": latest_text
    }



    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
