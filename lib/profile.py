import grequests
from bs4 import BeautifulSoup
from Dummy_user import Dummy_user


def get_profile_data(uname):
    profile_url = 'http://codeforces.com/profile/' + uname
    unsent_request = (grequests.get(url) for url in [profile_url])
    results = grequests.map(unsent_request)[0]
    soup = BeautifulSoup(results.text, 'html.parser')

    title = soup.find_all('div', {'class': 'user-rank'})[0].get_text().strip()

    info_div = soup.find_all('div', {'class': 'info'})[0].find_all('ul')[0].find_all('li')
    """
    0: ratings max and current
    2: friendds of n users
    4: registered when
    """
    current_rating = info_div[0].find_all('span')[0].get_text().strip()
    max_title = info_div[0].find_all('span')[1].find_all('span')[0].get_text().strip()[:-1]
    max_rating = info_div[0].find_all('span')[1].find_all('span')[1].get_text().strip()
    friends = info_div[2].get_text().strip().split(":")[-1].strip().split()[0]
    reg_date = info_div[4].find_all('span')[0].get_text().strip()

    if(not uname in soup.get_text()):
        return None,None,None

    return Dummy_user(uname,title,current_rating,max_rating,max_title,friends,reg_date)


if(__name__=="__main__"):
    uname='srbcheema1'
    from sys import argv
    if(len(argv)==2):
        uname = argv[1]
    dummy_user = get_profile_data(uname)
    dummy_user.print_data()

