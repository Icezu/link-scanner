from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from furl import furl
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request

def get_links(url: str):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    url_list = []
    url_without_dupe = []
    links = driver.find_elements(By.TAG_NAME, "a")
    # append links to list with no duplicate
    for i in links:
        if i not in url_list:  # Check for duplicate links
            attr = i.get_attribute('href') 
            split_link = furl(attr).remove(args=True, fragment=True).url  # remove fragments and query param
            url_list.append(split_link)
    # When appending into url_list, there will be some duplicate because 
    # it was split in split_link i.e. https://www.youtube.com/watch?v=CNOn3owCMLY
    # will be just https://www.youtube.com and all hyperlink in the list will be
    # just https://www.youtube.com 
    [url_without_dupe.append(x) for x in url_list if x not in url_without_dupe]
    return url_without_dupe

def is_valid_url(url: str):
    """Test if a url is valid & reachable"""
    # The connection is closed as soon as you receive your response
    # so you don't need to close the connection yourself.
    status_code = urllib.request.urlopen(url).getcode()
    if status_code == 200:
        return True

# print(get_links('https://www.youtube.com/'))
# print(is_valid_url('https://www.facebook.com'))
