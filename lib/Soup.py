import grequests
from bs4 import BeautifulSoup


'''
takes url and return soup.
returns None if there is bad connection or bad response code.
'''
def get_soup(url):
    unsent_requests = (grequests.get(url) for url in [url])
    result = grequests.map(unsent_requests)[0]
    if(result is None or result.status_code is not 200):
        return None
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup
