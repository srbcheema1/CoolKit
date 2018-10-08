#!/usr/bin/env python3
import time
import os
import subprocess as sp

try:
    from bs4 import BeautifulSoup
    import click
    import requests
    from robobrowser import RoboBrowser
    from terminaltables import AsciiTable
    import texttable
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback
    traceback.print_exc()
    print(err)
    sys.exit(0)


class Standing:
    def __init__(self,c_name,username,password,force_stdout=False):
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


@click.command()
@click.argument('c_name')
@click.argument('username')
@click.argument('password')
def tester(c_name,username,password,force_stdout=False):
    temp_Standing = Standing(c_name,username,password,force_stdout)
    temp_Standing.show()

if __name__ == '__main__':
    tester()
