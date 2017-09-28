#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

def _build_query(name):
    return "http://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=tt".format(quote(name).replace("%20", "+"))

def main():
    query = _build_query(sys.argv[1])
    soup = BeautifulSoup(requests.get(query).text, 'lxml')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("One command line argument required... exiting")
        sys.exit(1)
    else:
        sys.exit(main())