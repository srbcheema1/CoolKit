#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import subprocess as sp
import time

try:
    import click
    import getpass
    import requests

    from argparse import ArgumentParser
    from argcomplete import autocomplete
    from bs4 import BeautifulSoup
    from robobrowser import RoboBrowser
    from terminaltables import AsciiTable
    import texttable
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)


class Friends:
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def show(self):
        browser = RoboBrowser(parser = 'html.parser')
        browser.open('http://codeforces.com/enter')
        enter_form = browser.get_form('enterForm')
        enter_form['handleOrEmail'] = self.username
        enter_form['password'] = self.password
        browser.submit_form(enter_form)

        try:
            checks = list(map(lambda x: x.getText()[1:].strip(),
                browser.select('div.caption.titled')))
            if self.username not in checks:
                click.secho('Login Failed.. Wrong password.', fg = 'red')
                return
        except Exception as e:
            click.secho('Login Failed.. Maybe wrong id/password.', fg = 'red')
            return

        browser.open('http://codeforces.com/friends')
        soup = browser.parsed()[0] # no need of soup
        ftable = soup.findAll('div',{'class':'datatable'})[0].findAll('table')[0].findAll('tr')[1:]

        friends = [x.findAll('td')[1].getText().strip() for x in ftable]
        for f in friends:
            print(f)


class Standing:
    def __init__(self,c_name,username,password):
        self.c_name = c_name
        self.username = username
        self.password = password

    def show(self):
        browser = RoboBrowser(parser = 'html.parser')
        browser.open('http://codeforces.com/enter')
        enter_form = browser.get_form('enterForm')
        enter_form['handleOrEmail'] = self.username
        enter_form['password'] = self.password
        browser.submit_form(enter_form)

        try:
            checks = list(map(lambda x: x.getText()[1:].strip(),
                browser.select('div.caption.titled')))
            if self.username not in checks:
                click.secho('Login Failed.. Wrong password.', fg = 'red')
                return
        except Exception as e:
            click.secho('Login Failed.. Maybe wrong id/password.', fg = 'red')
            return

        browser.open('http://codeforces.com/contest/'+self.c_name+'/standings/friends/true')
        soup = browser.parsed()[0] # no need of soup
        ftable = soup.findAll('table',{'class':'standings'})[0].findAll('tr')[1:-1]
        tableh = soup.findAll('table',{'class':'standings'})[0].findAll('tr')[0].findAll('th')

        table_data = [[x.getText().strip() for x in tableh]]
        for friend in ftable:
            row = [x.getText().strip() for x in friend.findAll('td')]
            table_data += [row]

        tt = texttable.Texttable()
        tt.add_rows(table_data)
        tt.set_cols_valign(["b"]*len(tableh))
        print(tt.draw())


def create_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='first_arg')

    friends_parser = subparsers.add_parser('friends')
    friends_parser.add_argument('-u',"--user",
                                default=None,
                                help="username/handle")
    friends_parser.add_argument('-p',"--pswd",
                                default=None,
                                help="password")

    standing_parser = subparsers.add_parser('standings')
    standing_parser.add_argument('-c',"--contest",
                                default=None,
                                help="contest")
    standing_parser.add_argument('-u',"--user",
                                default=None,
                                help="username/handle")
    standing_parser.add_argument('-p',"--pswd",
                                default=None,
                                help="password")

    autocomplete(parser)
    return parser


def friend_tester(username,password):
    temp_friends = Friends(username,password)
    temp_friends.show()


def standing_tester(c_name,username,password):
    temp_Standing = Standing(c_name,username,password)
    temp_Standing.show()


if __name__ == '__main__':
    parser = create_parser()

    pars_args = parser.parse_args()
    username = pars_args.user
    password = pars_args.pswd
    if(not username):
        username = input('Please enter your username : ')
    if(not password):
        password = getpass.getpass('Enter your password : ')

    first_arg = pars_args.first_arg
    if first_arg == 'friends':
        friend_tester(username,password)
    elif first_arg == 'standings':
        c_name = pars_args.contest
        if(not c_name):
            c_name = input('Please enter contest name : ')
        standing_tester(c_name,username,password)
    else:
        print('unknown option')

