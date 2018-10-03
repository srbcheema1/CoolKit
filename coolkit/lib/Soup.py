import sys

try:
    import grequests
    from bs4 import BeautifulSoup
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback
    traceback.print_exc()
    print(err)
    sys.exit(0)

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
                    print(Colour.RED + 'please check your internet connection' + Colour.END)
            else:
                print(Colour.RED+'soup result on '+url+' :'+Colour.END,result)
            return None
        soup = BeautifulSoup(result.text, 'html.parser')
        return soup
