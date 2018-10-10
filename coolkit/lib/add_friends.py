#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import time

try:
    import click
    import getpass

    from argparse import ArgumentParser
    from argcomplete import autocomplete
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)

class Add_friends():
    def get_user_list(file_path):
        if(not file_path):
            return []

        user_list = []
        if(not os.path.isfile(file_path)):
            click.secho('path not found '+file_path,fg='red')
            sys.exit(1)
        with open(file_path,'r') as fin:
            lines = fin.readlines()
        user_list = [user.strip() for user in lines]
        return user_list


    def get_browser(hidden=False):
        options = webdriver.FirefoxOptions()
        if(hidden):
            options.add_argument('--headless')
            browser = webdriver.Firefox(firefox_options=options)
        else:
            browser = webdriver.Firefox()
        return browser


    def login_codeforces(browser,uname=None,pswd=None):
        browser.get('https://codeforces.com/enter')
        mail_box = browser.find_element_by_id('handleOrEmail')
        pswd_box = browser.find_element_by_id('password')

        if(not uname):
            uname = input('Enter your username/email : ')
        if(not pswd):
            pswd = getpass.getpass('Enter your password : ')

        mail_box.send_keys(uname)
        pswd_box.send_keys(pswd)
        pswd_box.send_keys(Keys.ENTER)

        LogoutButton = EC.presence_of_element_located((By.LINK_TEXT, 'Logout'))
        try:
            WebDriverWait(browser,5).until(LogoutButton)
        except TimeoutException:
            print("Loading took too much time!")
            sys.exit(1)


    def add_friends(browser,user_list=[],ignore_list=[],force=False):
        for user_id in user_list:
            browser.get('http://codeforces.com/profile/'+user_id)
            star = browser.find_element_by_class_name('friendStar')
            is_friend = False if 'addFriend' in star.get_attribute('class') else True
            if(user_id in ignore_list):
                print('ignoring '+user_id)
                continue
            if(not is_friend):
                if(not force):
                    inp = input('do you want to add '+user_id+' as a friend, y/n : ')
                else:
                    inp = 'y'
                if(inp in ['y','Y']):
                    star.click()
                    print('added '+user_id+' as friend')
            else:
                print(user_id+' is already your friend')


def create_parser():
    parser = ArgumentParser()

    parser.add_argument('-u',"--user",
                        default=None,
                        help="username/handle")
    parser.add_argument('-p',"--pswd",
                        default=None,
                        help="password")
    parser.add_argument('-i',"--input",
                        required=True,
                        help="file containing user list")
    parser.add_argument('-e',"--exclude",
                        default=None,
                        help="exclude list")
    parser.add_argument('-f',"--force",
                        default=False,
                        help="Add users without asking")
    autocomplete(parser)
    return parser



if __name__ == "__main__":
    parser = create_parser()

    pars_args = parser.parse_args()
    user_list = Add_friends.get_user_list(pars_args.input)
    ignore_list = Add_friends.get_user_list(pars_args.exclude)

    username = pars_args.user
    password = pars_args.pswd
    if(not username):
        username = input('Please enter your username : ')
    if(not password):
        password = getpass.getpass('Enter your password : ')

    browser = Add_friends.get_browser(hidden = True)
    Add_friends.login_codeforces(browser,username,password)
    Add_friends.add_friends(browser,user_list,ignore_list,force=False)
