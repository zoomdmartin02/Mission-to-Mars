
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Initialize browser, create data dictionary and end the WebDriver and return the scraped data.
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=False)

    # set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
    

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
   
    return news_title, news_p

# ### Featured Images
# 
def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        #img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url    

def mars_facts():
    # use 'read_html' to scrape the facts table into a dataframe
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'value']
    df.set_index('Description', inplace=True)
   
    # Convert dataframe into HTML format, add bootstrap

    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    image_urls = []
    titles = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    mars_hemispheres_soup = soup(html, 'html.parser')
    product_list = mars_hemispheres_soup.find_all('div', class_='description')
    base_url = 'https://astrogeology.usgs.gov'
    # product_list

    # loop through product_list
    for product in product_list:
        link = product.a['href']
        prod_title = product.h3.text
        titles.append(prod_title)
        # goto link for summary page
        browser.visit(base_url + link)

        # Find and click the open full image button
        open_full_image_button = browser.find_by_id('wide-image-toggle')
        open_full_image_button.click()

        # Find the relative image url
        html = browser.html
        image_soup = soup(html, 'html.parser')
        image_container = image_soup.find_all('div', class_='downloads')
        
        for image_url in image_container:
            url_link = image_url.a['href']
            image_urls.append(url_link)
        
        
            
    how_many = len(image_urls)

    for i in range(how_many):
        new_record = {'image_url': image_urls[i], 'title' : titles[i]}
        hemisphere_image_urls.append(new_record)


    return hemisphere_image_urls

