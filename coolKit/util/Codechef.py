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


class Codechef:
    """
    Class to handle downloading of test cases from Codechef
    """

    def __init__(self, args):
        self.site = args['site']
        self.contest = args['contest']
        self.problem = args['problem']
        self.force_download = args['force']

    def parse_html(self, req):
        """
        Method to parse the html and get test cases
        from a codechef problem
        """
        try:
            data = json.loads(req.text)
            soup = bs(data['body'], 'html.parser')
        except (KeyError, ValueError):
            print 'Problem not found..'
            Utilities.handle_kbd_interrupt(
                self.site, self.contest, self.problem)
            sys.exit(0)

        test_cases = soup.findAll('pre')
        formatted_inputs, formatted_outputs = [], []

        input_list = [
            '<pre>(.|\n)*<b>Input:?</b>:?',
            '<b>Output:?</b>(.|\n)+</pre>'
        ]

        output_list = [
            '<pre>(.|\n)+<b>Output:?</b>:?',
            '</pre>'
        ]

        input_regex = re.compile('(%s)' % '|'.join(input_list))
        output_regex = re.compile('(%s)' % '|'.join(output_list))

        for case in test_cases:
            inp = input_regex.sub('', str(case))
            out = output_regex.sub('', str(case))

            inp = re.sub('<[^<]+?>', '', inp)
            out = re.sub('<[^<]+?>', '', out)

            formatted_inputs += [inp.strip()]
            formatted_outputs += [out.strip()]

        # print 'Inputs', formatted_inputs
        # print 'Outputs', formatted_outputs

        return formatted_inputs, formatted_outputs

    def get_problem_links(self, req):
        """
        Method to get the links for the problems
        in a given codechef contest
        """
        soup = bs(req.text, 'html.parser')

        table = soup.find('table', {'class': 'dataTable'})

        if table is None:
            print 'Contest not found..'
            Utilities.handle_kbd_interrupt(
                self.site, self.contest, self.problem)
            sys.exit(0)

        links = [div.find('a')['href']
                 for div in table.findAll('div', {'class': 'problemname'})]
        links = ['https://codechef.com/api/contests/' + self.contest +
                 '/problems/' + link.split('/')[-1] for link in links]

        return links

    def handle_batch_requests(self, links):
        """
        Method to send simultaneous requests to
        all problem pages
        """
        rs = (grq.get(link) for link in links)
        responses = grq.map(rs)

        # responses = []
        # for link in links:
        #     responses += [rq.get(link)]

        failed_requests = []

        for response in responses:
            if response is not None and response.status_code == 200:
                inputs, outputs = self.parse_html(response)
                self.problem = response.url.split('/')[-1]
                Utilities.check_cache(self.site, self.contest, self.problem)
                Utilities.store_files(
                    self.site, self.contest, self.problem, inputs, outputs)
            else:
                failed_requests += [response.url]

        return failed_requests

    def scrape_problem(self):
        """
        Method to scrape a single problem from codechef
        """
        print 'Fetching problem ' + self.contest + '-' + self.problem + ' from Codechef...'
        url = 'https://codechef.com/api/contests/' + \
            self.contest + '/problems/' + self.problem
        req = Utilities.get_html(url)
        inputs, outputs = self.parse_html(req)
        Utilities.store_files(self.site, self.contest,
                              self.problem, inputs, outputs)
        print 'Done.'

    def scrape_contest(self):
        """
        Method to scrape all problems from a given codechef contest
        """
        print 'Checking problems available for contest ' + self.contest + '...'
        url = 'https://codechef.com/' + self.contest
        req = Utilities.get_html(url)
        links = self.get_problem_links(req)

        print 'Found %d problems..' % (len(links))

        if not self.force_download:
            cached_problems = os.listdir(os.path.join(
                Utilities.cache_dir, self.site, self.contest))
            links = [link for link in links if link.split(
                '/')[-1] not in cached_problems]

        failed_requests = self.handle_batch_requests(links)
        if len(failed_requests) > 0:
            self.handle_batch_requests(failed_requests)

