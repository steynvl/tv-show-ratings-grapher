#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from collections import namedtuple

def get_episodes(show_id):

    Episode = namedtuple('Episode', 'ep name rating votes')

    soup = BeautifulSoup(requests.get('http://www.imdb.com/title/{}/epdate'.format(show_id)).text, 'lxml')

    info = soup.find(id='tn15content')
    if len(info.contents) <= 1:
        yield
    else:
        for row in info.table('tr')[1:]:
            yield Episode(*[td.get_text(strip=True) for td in row('td')[:4]])

def build_query(name):
    return "http://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=tt".format(quote(name).replace("%20", "+"))

def main():
    query = build_query(sys.argv[1])
    soup = BeautifulSoup(requests.get(query).text, 'lxml')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("One command line argument required... exiting")
        sys.exit(1)
    else:
        sys.exit(main())