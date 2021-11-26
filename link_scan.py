from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from furl import furl
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
from typing import List
import sys


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
    if 'http' not in url:
        url = 'https://' + url
    status_code = urllib.request.urlopen(url).getcode()
    if status_code == 200:
        return True


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.
    """
    invalid_list = []
    for url in urllist:
        try:
            is_valid_url(url)
        except:
            invalid_list.append(url)
    return invalid_list


def main():
    bad_link_list = []
    get_url = get_links(sys.argv[1])
    for urls in get_url:
        try:
            if is_valid_url(urls):
                print(urls)
        except:
            bad_link_list.append(urls)
    print("Bad Links:")
    for bad in bad_link_list:
        print(bad)
    

if __name__ == '__main__':
    main()
