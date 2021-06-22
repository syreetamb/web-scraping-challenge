from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    data = {}
    executable_path ={'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    mars_soup = soup(html, 'html.parser')

    try:
        news_break = mars_soup.select_one('div.list_text')
        data['title'] = news_break.find('div', class_='content_title').get_text()
        data['paragraph'] = news_break.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    url ='https://spaceimages-mars.com'
    browser.visit(url)
    html = browser.html
    image_soup = soup(html, 'html.parser')
    try:

        image_url_rel = image_soup.find('img', class_='headerimage fade-in').get('src') 

    except AttributeError:
        return None

    data['image']= f'https://spaceimages-mars.com/{image_url_rel}'
     
    try:
        data['facts'] = pd.read_html('https://galaxyfacts-mars.com/')[0].to_html()

    except BaseException:
        return None

    browser.visit('https://marshemispheres.com/')
    hemispheres = []
    for i in range(4):
        hemisphere = {}
        try:
            hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
            browser.find_by_css('a.itemLink h3')[i].click()
            hemisphere['url'] = browser.find_by_text('Sample')['href']

        except AttributeError:
            return None, None

        browser.back()
        hemispheres.append(hemisphere)
    browser.quit()
    data['hemispheres'] = hemispheres

    return data

if __name__ == "__main__":
    print(scrape)