#!/bin/env python3
import logging
from pprint import pprint

import click
import instagram_scraper
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()


@click.command()
@click.option('--ig-username')
@click.option('--ig-password')
@click.option('--hashtag', default='egmporto2022')
def main(ig_username, ig_password, hashtag):
    insta_scraper = instagram_scraper.InstagramScraper(
        login_user=ig_username, login_pass=ig_password,
        tag=True, username=hashtag
    )
    insta_scraper.authenticate_with_login()

    for i in insta_scraper.query_hashtag_gen(hashtag):
        pprint(i)
        break


if __name__ == '__main__':
    main(auto_envvar_prefix='_')
