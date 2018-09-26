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


class Hackerrank:
    """
    Class to handle downloading of test cases from Hackerrank
    """

    def __init__(self, args):
        self.site = args['site']
        self.contest = args['contest']
        self.problem = '-'.join(args['problem'].split()
                                ).lower() if args['problem'] is not None else None
        self.force_download = args['force']

    def parse_html(self, req):
        """
        Method to parse the html and get test cases
        from a hackerrank problem
        """

        try:
            data = json.loads(req.text)
            soup = bs(data['model']['body_html'], 'html.parser')
        except (KeyError, ValueError):
            print 'Problem not found..'
            Utilities.handle_kbd_interrupt(
                self.site, self.contest, self.problem)
            sys.exit(0)

        input_divs = soup.findAll('div', {'class': 'challenge_sample_input'})
        output_divs = soup.findAll('div', {'class': 'challenge_sample_output'})

        inputs = [input_div.find('pre') for input_div in input_divs]
        outputs = [output_div.find('pre') for output_div in output_divs]

        regex_list = [
            '<pre>(<code>)?',
            '(</code>)?</pre>'
        ]

        regex = re.compile('(%s)' % '|'.join(regex_list))

        formatted_inputs, formatted_outputs = [], []

        for inp in inputs:
            spans = inp.findAll('span')
            if len(spans) > 0:
                formatted_input = '\n'.join(
                    [span.decode_contents() for span in spans])
            else:
                formatted_input = regex.sub('', str(inp))

            formatted_inputs += [formatted_input.strip()]

        for out in outputs:
            spans = out.findAll('span')
            if len(spans) > 0:
                formatted_output = '\n'.join(
                    [span.decode_contents() for span in spans])
            else:
                formatted_output = regex.sub('', str(out))

            formatted_outputs += [formatted_output.strip()]

        # print 'Inputs', formatted_inputs
        # print 'Outputs', formatted_outputs

        return formatted_inputs, formatted_outputs

    def get_problem_links(self, req):
        """
        Method to get the links for the problems
        in a given hackerrank contest
        """

        try:
            data = json.loads(req.text)
            data = data['models']
        except (KeyError, ValueError):
            print 'Contest not found..'
            Utilities.handle_kbd_interrupt(
                self.site, self.contest, self.problem)
            sys.exit(0)

        links = ['https://www.hackerrank.com/rest/contests/' + self.contest +
                 '/challenges/' + problem['slug'] for problem in data]

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
                Utilities.store_files(
                    self.site, self.contest, self.problem, inputs, outputs)
            else:
                failed_requests += [response.url]

        return failed_requests

    def scrape_problem(self):
        """
        Method to scrape a single problem from hackerrank
        """
        print 'Fetching problem ' + self.contest + '-' + self.problem + ' from Hackerrank...'
        url = 'https://www.hackerrank.com/rest/contests/' + \
            self.contest + '/challenges/' + self.problem
        req = Utilities.get_html(url)
        inputs, outputs = self.parse_html(req)
        Utilities.store_files(self.site, self.contest,
                              self.problem, inputs, outputs)
        print 'Done.'

    def scrape_contest(self):
        """
        Method to scrape all problems from a given hackerrank contest
        """
        print 'Checking problems available for contest ' + self.contest + '...'
        url = 'https://www.hackerrank.com/rest/contests/' + self.contest + '/challenges'
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
