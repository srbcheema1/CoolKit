import requests
from bs4 import BeautifulSoup


def get_profile_data(uname):
    pro_url = 'http://codeforces.com/profile/' + uname
    profile = requests.get(pro_url)

    pro_content= profile.content
    pro_soup = BeautifulSoup(profile.content, 'html.parser')

    if(not uname in str(pro_content)):
        return "-","-","-"

    body=pro_soup.find_all('div', {'id': 'body'})
    page_cont= body[0].find_all('div', {'id':'pageContent'})
    main_body = page_cont[0].find_all('div', {'class': 'roundbox'})
    user_box = main_body[0].find_all('div', {'class': 'userbox'})
    info = user_box[0].find_all('div', {'class': 'info'})
    #main_info = info[0].find_all('div', {'class': 'main-info'})
    #rate = main_info[0].find_all('span', {'class': 'user-green'})
    lis_t = info[0].find_all('ul', recursive=False) #lis_t is ul
    lis_t_item = lis_t[0].find_all('li', recursive=False) #item is li

    rate= lis_t_item[0].find_all('span', {'class': 'user-green'})
    rating= rate[0].get_text()


    other= lis_t_item[0].find_all('span', {'class': 'smaller'})
    title= other[0].find_all('span', {'class': 'user-cyan'})

    title_text = title[0].get_text().strip()
    if(title_text[-1]==','):
        title_text = title_text[:-1]
    title_rank = title[1].get_text()

    return rating,title_text,title_rank


if(__name__=="__main__"):
    uname='srbcheema1'
    from sys import argv
    if(len(argv)==2):
        uname = argv[1]
    rating,title_text,title_rank = get_profile_data(uname)
    print("The contest rating of {} is {}" .format(uname,rating))
    print("Max: {} {} " .format(title_text, title_rank))
