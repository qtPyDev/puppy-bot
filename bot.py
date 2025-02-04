# puppy_bot

import bsky_client
from bot_logger import log
import bot_config as config

import schedule
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


reset_cache = False


User = namedtuple('User', 'username, password')


def authenticate_connection_to_bsky():
    user = User(args.username, args.password)
    profile = bsky_client.authenticate(user)

    return profile


def extract_from_list(lst):
    item = random.choice(lst)


def start_taskmaster(profile):
    print(f'taskmaster is running press [{config.CMD_ESC}] to stop...')
    log.info('taskmaster is running...')

    posts = bsky_client.query_feed(config.QUERY)

    bsky_client.send_post(profile, random.choice(config.LEXICON))
    bsky_client.like_post(random.choice(posts))
    bsky_client.repost_post(random.choice(posts))

    refresh_cache = schedule.every(20).minutes.do(
        set_reset_cache,
        True
    )

    schedule.every(30).minutes.do(
        bsky_client.send_post,
        profile,
        random.choice(config.LEXICON)
    )

    schedule.every(2).minutes.do(
        bsky_client.like_post,
        random.choice(posts)
    )

    schedule.every(5).minutes.do(
        bsky_client.repost_post,
        random.choice(posts)
    )

    while reset_cache is False:
        schedule.run_pending()
        sleep(1)

    restart_taskmaster()


def restart_taskmaster():
    log.info(f'restarting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    set_reset_cache(False)

    start_taskmaster(profile)


def set_reset_cache(value):
    reset_cache = value


def main():
    log.info(f'starting [{config.APP_NAME}]...')

    profile = authenticate_connection_to_bsky()

    start_taskmaster(profile)


if __name__ == '__main__':
    main()
