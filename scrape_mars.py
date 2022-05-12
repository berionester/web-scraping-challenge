# Dependencies and Set up
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# scrape all function 
def scrape_all():
    # the splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # the information from the page
    news_title, news_paragraph = scraped_news(browser)

    # dictionary from the scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraphs": news_paragraph,
        "images": scraped_img(browser),
        "facts": scraped_facts(browser),
        "hemispheres": scraped_hemispheres(browser),
        "lastModified": dt.datetime.now()
    }

    # stop the webbrowser 
    browser.quit()

    # the webdriver
    return marsData


# scrape the news page
def scraped_news(browser):
    # the mars website
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
   # the title
    news_title = slide_elem.find('div', class_='content_title').get_text()
    # the paragraph text
    news_paragraphs = slide_elem.find('div', class_='article_teaser_body').get_text()

    # return the paragraph and title info
    return news_title, news_paragraphs

# scrape the images page
def scraped_img(browser):
    
    # the spaceImage url
    space_img_url = 'https://spaceimages-mars.com/'
    browser.visit(space_img_url)
    
    #  the full image button
    full_image_link = browser.find_by_tag('button')
    #the full image url
    full_image_link[1].click()

    # parsing
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # the relative image
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # the absulate url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

# scrape through the facts page
def scraped_facts(browser):

    # the facts
    galaxy_url = 'https://galaxyfacts-mars.com/'
    browser.visit(galaxy_url)

    # the html
    html = browser.html
    facts_soup = soup(html, 'html.parser')

    # the location
    facts_Location = facts_soup.find('div', class_='diagram mt-4')
    # find the html code for the fact table
    facts_Table = facts_Location.find('table')

    # an empty string to add the text
    facts = ""
    facts += str(facts_Table)
    return facts

# scrape through the hemisphere page
def scraped_hemispheres(browser):
    #get hemisphere URL
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

    # the list of the images and titles
    hemisphere_img_url = []

    # loop for all pages
    for i in range(4):

        hemisphereInfo = {}
        # the element on each loop
        browser.find_by_css('a.product-item img')[i].click()
        sample_element = browser.find_by_text("Sample").first
        hemisphereInfo["img_url"] = sample_element["href"]
    
        # the hemisphere title
        hemisphereInfo["title"] = browser.find_by_css("h2.title").text
        hemisphere_img_url.append(hemisphereInfo)
        browser.back()

    return hemisphere_img_url

#  create a flask app
if __name__ == "__main__":
    print(scrape_all())