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


class Friends:
    def __init__(self,username,password,force_stdout=False):
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


@click.command()
@click.argument('username')
@click.argument('password')
def tester(username,password,force_stdout=False):
    temp_friends = Friends(username,password,force_stdout)
    temp_friends.show()

if __name__ == '__main__':
    tester()
