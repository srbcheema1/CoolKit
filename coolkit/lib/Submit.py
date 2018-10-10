#!/usr/bin/env python3

import os
import subprocess as sp
import time

try:
    import click
    import requests

    from robobrowser import RoboBrowser
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)


class Submit:
    notify_installed = True
    force_stdout = False

    def __init__(self,c_name,p_name,inputfile,username,password,force_stdout=False):
        self.c_name = c_name
        self.p_name = p_name
        self.prob_id = c_name + p_name
        self.inputfile = inputfile
        self.username = username
        self.password = password
        Submit.notify_installed = Submit._is_installed_notify()
        Submit.force_stdout = force_stdout
        if(force_stdout):
            notify_installed = False

    @staticmethod
    def get_latest_verdict(user):
        req = 'http://codeforces.com/api/user.status?'+'handle='+user+'&from=1&count=1'
        r = requests.get(req)
        js = r.json()
        if 'status' not in js or js['status'] != 'OK':
            click.secho("unable to connect, try it yourself : "+req,fg='red')
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

        browser.open('http://codeforces.com/contest/'+self.c_name+'/submit')
        submit_form = browser.get_form(class_ = 'submit-form')
        submit_form['submittedProblemIndex'].value = self.p_name
        submit_form['sourceFile'] = self.inputfile

        browser.submit_form(submit_form)
        print(browser.url)
        # if browser.url[-6:] != 'status': # it was used when submitting from problemset
        if not 'my' in browser.url:
            click.secho('Failed submission, probably you have submit the same file before', fg = 'red')
            return

        Submit.print_verdict(last_id,self.username,100)
        click.secho('[{0}] submitted ...'.format(self.inputfile), fg = 'green')



    def daemon(func):
        def wrapper(*args, **kwargs):
            if(Submit.force_stdout):
                '''
                in case nofify is not installed it wont run like demon
                '''
                return func(*args,**kwargs)

            if os.fork():
                '''
                main process has value positive while fork has 0
                returning in main process, so no function executed
                '''
                return
            '''
            child process will run this function and return
            as child process is invisible it wont be visible
            but will keep on running after parent finishes
            '''
            func(*args, **kwargs)
            os._exit(os.EX_OK)
        return wrapper

    @daemon
    def print_verdict(last_id,username,max_time = 100,notify_installed = True):
        hasStarted = False
        while True:
            id_, verdict_, time_, memory_, passedTestCount_ = Submit.get_latest_verdict(username)
            if id_ != last_id and verdict_ != 'TESTING' and verdict_ != None:
                if verdict_ == 'OK':
                    message = 'OK - Passed ' + str(passedTestCount_) + ' tests'
                    color = 'green'
                else:
                    message = verdict_ + ' on ' + str(passedTestCount_+1) + ' test'
                    color = 'red'
                if(Submit.notify_installed): sp.call(['notify-send','Codeforces',message])
                elif(Submit.force_stdout): click.secho(message,color)
                break
            elif verdict_ == 'TESTING' and (not hasStarted):
                message = 'Judgement has begun'
                if(Submit.notify_installed): sp.call(['notify-send','Codeforces',message])
                elif(Submit.force_stdout): click.secho(message,'green')
                hasStarted = True
            time.sleep(0.5)
            max_time -= 1
            if(max_time < 0):
                message = 'Time out'
                if(Submit.notify_installed): sp.call(['notify-send','Codeforces',message])
                elif(Submit.force_stdout): click.secho(message,'yellow')
                break

    def _is_installed_notify():
        try:
            sp.call(['notify-send','--help'],stdout=sp.PIPE)
            return True
        except:
            click.secho('notify-send seems not working, please install notify-send',fg='red')
            return False

@click.command()
@click.argument('c_name')
@click.argument('p_name')
@click.argument('inputfile')
@click.argument('username')
@click.argument('password')
def tester(c_name,p_name, inputfile,username,password,force_stdout=False):
    if(not os.path.exists(inputfile)):
        click.secho('file '+inputfile+' doesnot exists',fg='red')
        return
    temp_submit = Submit(c_name,p_name,inputfile,username,password,force_stdout)
    temp_submit.submit()

if __name__ == '__main__':
    tester()
