import sys
import json
import re
import os
try:
    from bs4 import BeautifulSoup as bs
    import requests as rq
    import grequests as grq
    from argparse import ArgumentParser
except:
    err = """
    You haven't installed the required dependencies.
    Run 'python setup.py install' to install the dependencies.
    """
    print err
    sys.exit(0)

import util

class Codeforces:
    """
    Class to handle downloading of test cases from Codeforces
    Methods:
        parse_html
        get_problem_links(self, req):
        handle_batch_requests(self, links):
        handle_batch_requests(self, links):
        scrape_problem(self):
        scrape_contest(self):

    """
    def __init__(self, args):
        self.site = args['site']
        self.contest = args['contest']
        self.problem = args['problem']
        self.force_download = args['force']

    def parse_html(self, req):
        """
        Method to parse the html and get test cases
        from a codeforces problem
        return formatted_inputs , formatted_outputs
        """
        soup = bs(req.text, 'html.parser')

        inputs = soup.findAll('div', {'class': 'input'})
        outputs = soup.findAll('div', {'class': 'output'})

        if len(inputs) == 0 or len(outputs) == 0:
            print 'Problem not found..'
            Utilities.handle_kbd_interrupt(
                self.site, self.contest, self.problem)
            sys.exit(0)

        repls = ('<br>', '\n'), ('<br/>', '\n'), ('</br>', '')

        formatted_inputs, formatted_outputs = [], []
        for inp in inputs:
            pre = inp.find('pre').decode_contents()
            pre = reduce(lambda a, kv: a.replace(*kv), repls, pre)
            pre = re.sub('<[^<]+?>', '', pre)
            formatted_inputs += [pre]
        for out in outputs:
            pre = out.find('pre').decode_contents()
            pre = reduce(lambda a, kv: a.replace(*kv), repls, pre)
            pre = re.sub('<[^<]+?>', '', pre)
            formatted_outputs += [pre]

        return formatted_inputs, formatted_outputs

    def get_problem_links(self, req):
        """
        Method to get the links for the problems
        in a given codeforces contest
        """
        soup = bs(req.text, 'html.parser')
        table = soup.find('table', {'class': 'problems'})
        if table is None:
            print 'Contest not found..'
            Utilities.handle_kbd_interrupt(
                self.site, self.contest, self.problem)
            sys.exit(0)
        links = ['http://codeforces.com' + td.find('a')['href'] for td in table.findAll('td', {'class': 'id'})]
        return links

    def handle_batch_requests(self, links):
        """
        Method to send simultaneous requests to
        all problem pages
        """
        rs = (grq.get(link) for link in links)
        responses = grq.map(rs)

        failed_requests = []
        for response in responses:
            if response is not None and response.status_code == 200:
                inputs, outputs = self.parse_html(response)
                self.problem = response.url.split('/')[-1]
                Utilities.check_cache(self.site, self.contest, self.problem)
                Utilities.store_files(self.site, self.contest, self.problem, inputs, outputs)
            else:
                failed_requests += [response.url]
        return failed_requests

    def scrape_problem(self):
        """
        Method to scrape a single problem from codeforces
        """
        print 'Fetching problem ' + self.contest + '-' + self.problem + ' from Codeforces...'
        type_of_contest = 'contest' if int(self.contest) <= 100000 else 'gym'
        url = 'http://codeforces.com/%s/%s/problem/%s' % (type_of_contest, self.contest, self.problem)
        req = Utilities.get_html(url)
        inputs, outputs = self.parse_html(req)
        Utilities.store_files(self.site, self.contest, self.problem, inputs, outputs)
        print 'Done.'

    def scrape_contest(self):
        """
        Method to scrape all problems from a given codeforces contest
        """
        print 'Checking problems available for contest ' + self.contest + '...'
        type_of_contest = 'contest' if int(self.contest) <= 100000 else 'gym'
        url = 'http://codeforces.com/%s/%s' % (type, self.contest)
        req = Utilities.get_html(url)
        links = self.get_problem_links(req)
        print 'Found %d problems..' % (len(links))

        if not self.force_download:
            cached_problems = os.listdir(os.path.join(Utilities.cache_dir, self.site, self.contest))
            links = [link for link in links if link.split('/')[-1] not in cached_problems]

        failed_requests = self.handle_batch_requests(links)
        if len(failed_requests) > 0:
            self.handle_batch_requests(failed_requests)
