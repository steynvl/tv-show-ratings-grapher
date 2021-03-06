#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


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
    return 'http://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=tt'.format(quote(name))


def get_show_id(query):
    soup = BeautifulSoup(requests.get(query).text, 'lxml')

    table = soup.find('table', 'findList')

    if table is None:
        return

    result = table.findAll('a')[1]
    show_name = result.contents[0]
    result = result['href']
    show_id = result[7:result.index('/', 7)]
    return show_id, show_name


def apply_linear_regression(x, y):
    slope, intercept, _, _, _ = linregress(x, y)
    return slope, intercept


def plot_data(episodes, show_name):
    x = np.arange(len(episodes))
    y = [np.float(ep.rating) for ep in episodes]

    slope, intercept = apply_linear_regression(x, y)

    plt.figure()
    plt.scatter(x, y, label='Every Episode')
    plt.plot(x, intercept + slope*x, label='Linear Regression of all Episodes')
    plt.title('{} IMDB ratings per episode'.format(show_name))
    plt.xlabel('Episodes')
    plt.ylabel('Rating per Episode')

    axes = plt.gca()
    axes.set_ylim([0, 10])

    plt.show()


def main():
    name = ' '.join(sys.argv[1:]).strip()
    query = build_query(name)

    info = get_show_id(query)

    if info is None:
        print('No results found for {}\n'.format(name))
        sys.exit(1)

    show_id, show_name = info

    episodes = list(get_episodes(show_id))

    if episodes[0] is None:
        print('{} is not a tv show!'.format(name))
        sys.exit(1)

    plot_data(episodes, show_name)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: python3 tv_show.py <tv_show_name>')
        sys.exit(2)
    else:
        sys.exit(main())
