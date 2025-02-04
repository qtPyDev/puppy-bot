# puppy_bot

import bsky_client
from bot_logger import log
import bot_config as config

import random
from collections import namedtuple
from time import sleep
import argparse

parser = argparse.ArgumentParser('puppy_bot')
parser.add_argument(
    'username',
    help='the username of the bot account',
    metavar='-u',
    type=str
)
parser.add_argument(
    'password',
    help='the password of the bot account',
    metavar='-p',
    type=str
)
args = parser.parse_args()



User = namedtuple('User', 'username, password')


def authenticate_connection_to_bsky():
    user = User(args.username, args.password)
    profile = bsky_client.authenticate(user)

    return profile


def start_taskmaster(profile):
    print(f'taskmaster is running press [{config.CMD_ESC}] to stop...')
    log.info('taskmaster is running...')

    posts = bsky_client.query_feed(config.QUERY)

    bsky_client.send_post(profile, random.choice(config.LEXICON))

    for post in posts:
        bsky_client.like_post(post)
        sleep(30)
        bsky_client.repost_post(post)
        sleep(270)

    restart_taskmaster()


def restart_taskmaster():
    log.info(f'restarting [{config.APP_NAME}]...')
    print(f'restarting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    start_taskmaster(profile)


def main():
    log.info(f'starting [{config.APP_NAME}]...')
    print(f'starting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    start_taskmaster(profile)


if __name__ == '__main__':
    main()
