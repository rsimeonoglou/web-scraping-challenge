from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd




def scrape():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
   
    latest_title, latest_text = news(browser)


    mars_data = {
        "latest_title": latest_title,
        "latest_text": latest_text,
        "featured_image": featured_image(browser),
        "facts": mars_facts(browser),
        "hemispheres": hemispheres(browser)
    }

    
    return mars_data

def news(browser):

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

    return latest_title, latest_text

def featured_image(browser):

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('img', class_='headerimage fade-in')['src']
    parsed_url = url.split('/')
    featured_image_url = parsed_url[0]+'//'+ parsed_url[1] + '/' + parsed_url[2] + '/' + parsed_url[3] + '/'+ image

    return featured_image_url

def mars_facts(browser):
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    html_table = df.to_html(classes="table table-striped")
    return html_table

def hemispheres(browser):

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

    return hemisphere_image_urls


    
if __name__ == "__main__":


    print(scrape())
