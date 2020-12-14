def hemispheres():
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
        
        
    for x in image_urls:
        for y in titles:
            my_dicts = {  
                    'image_url': x,
                    'title': y
                }
            
        hemisphere_image_urls.append(my_dicts)

    return hemisphere_image_urls
