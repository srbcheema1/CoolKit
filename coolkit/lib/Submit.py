import time
import os
import subprocess as sp

try:
    import click
    import requests
    from robobrowser import RoboBrowser
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback
    traceback.print_exc()
    print(err)
    sys.exit(0)

from .Colour import Colour


class Submit:
    def __init__(self,prob_id,inputfile,username,password):
        self.prob_id = prob_id
        self.inputfile = inputfile
        self.username = username
        self.password = password

    @staticmethod
    def get_latest_verdict(user):
        r = requests.get('http://codeforces.com/api/user.status?' +
                         'handle={}&from=1&count=1'.format(user))
        js = r.json()
        if 'status' not in js or js['status'] != 'OK':
            raise ConnectionError('Cannot connect to codeforces!')
        try:
            result = js['result'][0]
            id_ = result['id']
            verdict_ = result.get('verdict',None)
            time_ = result['timeConsumedMillis']
            memory_ = result['memoryConsumedBytes'] / 1000
            passedTestCount_ = result['passedTestCount']
        except Exception as e:
            raise ConnectionError('Cannot get latest submission, error')
        return id_, verdict_, time_, memory_, passedTestCount_


    def submit(self):
        # get latest submission id, so when submitting should have not equal id
        last_id, b, c, d, e = Submit.get_latest_verdict(self.username)

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

        browser.open('http://codeforces.com/problemset/submit')
        submit_form = browser.get_form(class_ = 'submit-form')
        submit_form['submittedProblemCode'] = self.prob_id
        submit_form['sourceFile'] = self.inputfile

        browser.submit_form(submit_form)
        if browser.url[-6:] != 'status':
            click.secho('Failed submission, probably you have submit the same file before', fg = 'red')
            return

        Submit.print_verdict(last_id,self.username,100)
        click.secho('[{0}] submitted ...'.format(self.inputfile), fg = 'green')


    def daemon(func):
        def wrapper(*args, **kwargs):
            if os.fork(): return
            func(*args, **kwargs)
            os._exit(os.EX_OK)
        return wrapper

    @daemon
    def print_verdict(last_id,username,max_time = 100):
        hasStarted = False
        notify_installed = True
        try:
            sp.call(['notify-send','--help'],stdout=sp.PIPE)
        except:
            print(Colour.YELLOW+'notify-send seems not working, please install notify-send'+Colour.END)
            notify_installed = False

        while True:
            id_, verdict_, time_, memory_, passedTestCount_ = Submit.get_latest_verdict(username)
            if id_ != last_id and verdict_ != 'TESTING' and verdict_ != None:
                if verdict_ == 'OK':
                    message = 'OK - Passed ' + str(passedTestCount_) + ' tests'
                else:
                    message = verdict_ + ' on ' + str(passedTestCount_+1) + ' test'
                if(notify_installed): sp.call(['notify-send','Codeforces',message])
                break
            elif verdict_ == 'TESTING' and (not hasStarted):
                message = 'Judgement has begun'
                if(notify_installed): sp.call(['notify-send','Codeforces',message])
                hasStarted = True
            time.sleep(0.5)
            max_time -= 1
            if(max_time < 0):
                message = 'Time out'
                if(notify_installed): sp.call(['notify-send','Codeforces',message])
                break


@click.command()
@click.argument('prob_id')
@click.argument('inputfile')
@click.argument('username')
@click.argument('password')
def tester(prob_id, inputfile,username,password):
    if(not os.path.exists(inputfile)):
        print(Colour.RED+"file "+inputfile+' doesnot exists'+Colour.END)
        return
    temp_submit = Submit(prob_id,inputfile,username,password)
    temp_submit.submit()

if __name__ == '__main__':
    tester()
