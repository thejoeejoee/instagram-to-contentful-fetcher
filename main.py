#!/bin/env python3
from pprint import pprint

import click
import instagram_scraper
import logging

logging.basicConfig(level=logging.DEBUG)


@click.command()
@click.argument('username')
@click.argument('password')
@click.argument('tag', default='egmporto2022')
def main(username, password, tag):
    insta_scraper = instagram_scraper.InstagramScraper(
        login_user=username, login_pass=password, tag=True, username=tag
    )
    insta_scraper.authenticate_with_login()

    for i in insta_scraper.query_hashtag_gen(tag):
        pprint(i)
        break

if __name__ == '__main__':
    main()
