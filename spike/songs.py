#! /usr/bin/env python3

import sys
import time

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_browser(hidden=False):
    options = webdriver.FirefoxOptions()
    if(hidden):
        options.add_argument('--headless')
        browser = webdriver.Firefox(firefox_options=options)
    else:
        browser = webdriver.Firefox()
    return browser

def get_song_link(query):
    url='https://www.youtube.com/results?search_query='+query
    source_code = requests.get(url, timeout=150)
    soup=BeautifulSoup(source_code.text,"html.parser")
    songs=soup.findAll('div',{'class':'yt-lockup-video'})
    song=songs[0].contents[0].contents[0].contents[0]
    link= 'https://www.youtube.com'+song['href']
    return link

def create_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='first_arg')

    play_parser = subparsers.add_parser('play')
    play_parser.add_argument("inp",nargs='*',
                            default = None,
                            help="song name")
    return parser

if __name__=='__main__':
    parser = create_parser()
    pars_args = parser.parse_args()

    first_arg = pars_args.first_arg
    if first_arg == 'play':
        song_name = 'end+harf+cheema'
        if(len(pars_args.inp)):
            song_name = '+'.join(pars_args.inp)
    else:
        song_name = 'end+harf+cheema'
        print('unknown option')

    song_link = get_song_link(song_name)
    browser = get_browser(hidden=False)
    browser.get(song_link)
