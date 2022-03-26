import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
import pprint 
from IPython.display import Markdown, display
import matplotlib.pyplot as plt
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:
def init_browser():
    executable_path = {"executable_path": "/Users/rolandoportal/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# In[3]:

def scrape():
    browser = init_browser()
    url = "https://redplanetscience.com"
    browser.visit(url)
    
# In[4]:

    # Create a Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #collect the latest News Title
    latest_title = soup.find('div',class_='content_title').text
    # collect the latest Paragraph Text
    latest_paragraph = soup.find('div',class_='article_teaser_body').text
    

    # JPL Mars Space Images - Featured Image

# In[5]:


    jpl_url = 'https://spaceimages-mars.com'
    jpl_url_root = jpl_url.split('/spaceimages')[0]
    browser.visit(jpl_url)


# In[6]:

    browser.links.find_by_partial_text('FULL')
    time.sleep(5)
    
# In[7]:

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")
    jpl_img_result = jpl_soup.find("img", class_="headerimage fade-in")
    jpl_img_result 


# In[8]:


    result=("/image/featured/mars1.jpg")


# In[9]:


# Make sure to save a complete url string for this image
    featured_image_url = f"https://spaceimages-mars.com{result}"
    print(f"Complete URL String:\n{featured_image_url}")
    


# ## Mars Facts

# In[10]:


    planet_url = 'https://galaxyfacts-mars.com'
    browser.visit(planet_url)


# In[11]:


    # Use Panda's `read_html` to parse the url
    planet_df = pd.read_html("https://galaxyfacts-mars.com")[0]
    print(planet_df)


# In[12]:


    # Clean up DataFrame, set index
    planet_df.columns=["Planet Profile", "Values Mars", "Values Earth"]
    planet_df.set_index("Planet Profile", inplace=True)
    planet_df


# In[13]:


    facts_html = planet_df.to_html()
    facts_html = facts_html.replace("\n","")
    facts_html


    # ## Mars Hemispheres

# In[14]:


    h_url = "https://marshemispheres.com/"
    h_url_root = h_url.split('/search')[0]
    browser.visit(h_url)


# In[15]:


    # Scrape the site and visit each hemisphere page
    title_list = []
    url_list = []
    
    for result in range(1):
        h_html = browser.html
        h_soup = BeautifulSoup(h_html, "html.parser")
        h_results = h_soup.find_all("div", class_="item")
    
        # Get url for each hemisphere
        for item in h_results:
            item_url = item.a["href"]
            item_full_url = h_url_root + item_url
            url_list.append(item_full_url)
            title = item.find("h3").text
            title_list.append(title)
        
# In[17]:


    url_dict_list = []

    for item_url in url_list:
        browser.visit(item_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        img_path = soup.select_one("ul")
        image_url = img_path.a["href"]
        url_dict_list.append(image_url)
        
    hemisphere_image_urls = []
    for url,title in zip(url_dict_list,title_list):
        hemisphere_image_dict = {}
        hemisphere_image_dict["title"] = title
        hemisphere_image_dict["img_url"] = h_url + url
        hemisphere_image_urls.append(hemisphere_image_dict)
    
# In[18]:


    
        
    # Return all results as one dictionary
    mars_data_dict = {
        "latest_title" : latest_title,
        "latest_paragraph" : latest_paragraph,
        "featured_image_url" : featured_image_url,
        "hemisphere_image" : hemisphere_image_urls

        
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return(mars_data_dict)







