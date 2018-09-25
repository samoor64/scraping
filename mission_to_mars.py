
# coding: utf-8

# In[1]:


# Dependencies
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests
import pandas as pd
import lxml.html as LH


# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser_mars = Browser('chrome', **executable_path, headless=False)
browser_jpl = Browser('chrome', **executable_path, headless=False)
browser_twitter = Browser('chrome', **executable_path, headless=False)
browser_marsFacts = Browser('chrome', **executable_path, headless=False)


# In[3]:


#Visit Different URLs

mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser_mars.visit(mars_url)

jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser_jpl.visit(jpl_url)

marsTwitter_url = 'https://twitter.com/marswxreport?lang=en'
browser_twitter.visit(marsTwitter_url)

marsFacts_url = 'https://space-facts.com/mars/'
browser_marsFacts.visit(marsFacts_url)

# usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
# browser_usgs.visit(usgs_url)


# In[4]:


#Create Beautiful Soups
mars_soup = bs(browser_mars.html, 'lxml')
jpl_soup = bs(browser_jpl.html, 'lxml')
twitter_soup = bs(browser_twitter.html, 'lxml')
facts_soup = bs(browser_marsFacts.html, 'lxml')
# usgs_soup = bs(browser_usgs.html, 'lxml')


# In[5]:


#Find Most Recent Mars Article
titles = mars_soup.find('div', class_='content_title').text
content = mars_soup.find('div', class_ = 'article_teaser_body').text
print('Title: ' + titles)
print(' ')
print('Description: ' + content)


# In[6]:


#Find Featured Image Link
jpl_image = browser_jpl.find_by_id('full_image')
jpl_image.click()


# In[7]:


browser_jpl.is_element_present_by_text('more info', wait_time=1)
more_info_jpl = browser_jpl.find_link_by_partial_text('more info')
more_info_jpl.click()


# In[8]:


html_jpl = browser_jpl.html
img_jpl = bs(html_jpl, 'lxml')


# In[9]:


another_jpl_img = img_jpl.select_one('figure.lede a img').get('src')
print(another_jpl_img)


# In[10]:


featured_img_url = 'https://www.jpl.nasa.gov'+ another_jpl_img
print(featured_img_url)


# In[11]:


#Find Mars Weather
attrs = {"class": "tweet", "data-name": "Mars Weather"}
tweet = twitter_soup.find('div', attrs=attrs)
mars_weather = tweet.find('p', class_='TweetTextSize').text
print(mars_weather)


# In[12]:


#Find Mars Facts and create df
mars_facts_pd = pd.read_html(marsFacts_url)
mars_facts_pd


# In[13]:


usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser_usgs = Browser('chrome', **executable_path, headless=False)
browser_usgs.visit(usgs_url)

usgs_soups = bs(browser_usgs.html, 'lxml')
print(browser_usgs.url)


# In[15]:


url_list = set()

usgs_go_next = browser_usgs.find_by_css('a.itemLink.product-item')

for link in usgs_go_next:
    url_list.add(link['href'])
print(url_list)


# In[17]:


for urls in url_list:
    browser_usgs.visit(urls)
    img_url = browser_usgs.find_by_css('div[class="downloads"] img')
    print(img_url['src'])
    


# In[18]:


browser_mars.quit()
browser_jpl.quit()
browser_twitter.quit()
browser_marsFacts.quit()
browser_usgs.quit()

