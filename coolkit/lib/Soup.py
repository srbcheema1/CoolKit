import sys

try:
    import grequests

    from bs4 import BeautifulSoup
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)

from .Colour import Colour

class Soup:
    def __init__():
        pass

    @staticmethod
    def get_soup(url):
        '''
        takes url and return soup.
        returns None if there is bad connection or bad response code.
        '''
        unsent_requests = (grequests.get(url) for url in [url])
        result = grequests.map(unsent_requests)[0]
        if(result is None or result.status_code is not 200):
            if(result == None):
                temp_unsent_requests = (grequests.get(url) for url in ['https://google.com'])
                temp_result = grequests.map(temp_unsent_requests)[0]
                if(temp_result == None):
                    Colour.print('please check your internet connection', Colour.RED)
            else:
                Colour.print('soup result on '+url+' :'+Colour.END+str(result), Colour.RED)
            return None
        soup = BeautifulSoup(result.text, 'html.parser')
        return soup
