#!/bin/env python3
import logging
import time
from pathlib import Path
from pprint import pprint

import click
import contentful_management
import instagram_scraper
import requests
from contentful_management.errors import NotFoundError
from dotenv import load_dotenv
from instagram_scraper import InstagramScraper

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

@click.command()
@click.option('--ig-username')
@click.option('--ig-password')
@click.option('--hashtag')
@click.option('--ctf-token')
def main(ig_username, ig_password, hashtag, ctf_token):
    instagram = InstagramScraper(
        login_user=ig_username, login_pass=ig_password,
        tag=True, username=hashtag, maximum=24, media_types=['image']
    )
    instagram.authenticate_with_login()

    contentful = contentful_management.Client(ctf_token, default_locale='en-US')

    space = contentful.spaces().find('zhy9qk1dr5mw')
    environment = space.environments().find('master')

    assets = []

    for post in instagram.query_hashtag_gen(hashtag, ):

        image_url = post.get('display_url')
        response = requests.get(image_url)

        asset_id = post.get('shortcode')
        try:
            environment.assets().find(asset_id)
        except NotFoundError:
            ...
        else:
            continue

        file_attributes = {
            'fields': {
                'title': {
                    'en-US': f'IG: {asset_id}'
                },
                'file': {
                    'en-US': {
                        'fileName': asset_id,
                        'contentType': response.headers.get('Content-type'),
                        'upload': post.get('display_url')
                    }
                }
            }
        }

        asset = environment.assets().create(
            asset_id,
            file_attributes
        )

        asset.process()
        assets.append(asset)

    for a in assets:
        # processing takes some time and ctf doesn't allow to publish it before it's processed
        while not a.url():
            time.sleep(1)
            a.reload()
        a.publish()



if __name__ == '__main__':
    main(auto_envvar_prefix='_')
