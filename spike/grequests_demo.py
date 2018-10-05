import grequests
import requests
from bs4 import BeautifulSoup

urls = ['http://google.com', 'http://yahoo.com', 'http://bing.com']

unsent_request = (grequests.get(url) for url in urls)

results = grequests.map(unsent_request)
# print(results)

# now our work

profile_url = 'http://codeforces.com/profile/' + 'srbcheema1'
urls = [profile_url]
unsent_request = (grequests.get(url) for url in urls)
result1 = grequests.map(unsent_request)
result2 = requests.get(profile_url)
# both things are almost same
print(result1[0])
print(result2)

soup = BeautifulSoup(result1[0].text, 'html.parser')

title = soup.find_all('div', {'class': 'user-rank'})[0].get_text().strip()
print(title, "is title")

info_div = soup.find_all('div', {'class': 'info'})[0].find_all('ul')[0].find_all('li')
"""
0: ratings max and current
2: friendds of n users
4: registered when
"""
current_rating = info_div[0].find_all('span')[0].get_text().strip()
max_title = info_div[0].find_all('span')[1].find_all('span')[0].get_text().strip()
max_rating = info_div[0].find_all('span')[1].find_all('span')[1].get_text().strip()
print("current_rating",current_rating)
print("max_rating",max_rating)
print("max_title",max_title)
friends = info_div[2].get_text().strip().split(":")[-1].strip().split()[0]
print("friends :",friends)
reg_date = info_div[4].find_all('span')[0].get_text().strip()
print("registered :",reg_date)
