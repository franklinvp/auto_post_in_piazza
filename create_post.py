#!/usr/bin/env python

import logging
from datetime import datetime
from json import load as json_load
from os import path as osPath
from sys import exit

from piazza_api import Piazza

SCRIPT_DIRECTORY = "."

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='create_post.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

logger.info('Running script')
today = datetime.today()

# Check if it was run today
today_date = today.strftime('%Y-%m-%d')
with open(
    osPath.join(SCRIPT_DIRECTORY, 'days_ran.txt'),
    'r',
    encoding='utf-8'
) as infile:
    if today_date in infile.read():
        logger.info('Post already created')
        exit(0)

# Record that it was run today
with open(
    osPath.join(SCRIPT_DIRECTORY, 'days_ran.txt'),
    'a',
    encoding='utf-8'
) as outfile:
    logger.info(f'Post created on {today_date}')
    outfile.write(f'{today_date}\n')

p = Piazza()
try:
    with open(
        osPath.join(SCRIPT_DIRECTORY, 'data'),
        'r',
        encoding='utf-8'
    ) as infile:
        x, y = infile.read().strip().split(',')
except Exception as _:
    logger.exception('Exception')
    exit(1)
try:
    # The line below can be
    # p.user_login()
    # which will prompt you to enter the email and password
    p.user_login(email=x, password=y)
    logger.info('Logging to Piazza')
except Exception as _:
    logger.info(f'{_}')
    logger.exception('Exception')
    exit(1)

# Have a file 'posts.json' with the contents of the posts to be written
# to Piazza in the form
#
# {
#   "YYYY-MM-DD": {
#     "subject": "The subject",
#      "content": "The content"
#   }
# }
#
# I am assuming the post content is written as Markdown.
# See below it being enclosed in <md></md>
posts = None
with open(
    osPath.join(SCRIPT_DIRECTORY, 'posts.json'),
    'r',
    encoding='utf-8'
) as infile:
    posts = json_load(infile, strict=False)
    logger.info('Got posts')
if posts is None:
    logger.info('posts is None')
    exit(0)

todays_posts = posts.get(today_date, [])

for post in todays_posts:
    # The class ID can be seen in the URL.
    # For example in https://piazza.com/class/m8lo7g5t4qv7ah
    # m8lo7g5t4qv7ah is the class ID
    classID = post.get("classID", None)
    if classID is None:
        continue
    test_class = p.network(classID)

    post_subject = post.get('subject', 'No subject')
    post_content = (
        f"<md>{post.get('content', '')}\n\n"
        "(automatically generated)</mn>"
    )
    try:
        test_class.create_post(
            post_type='note',
            post_folders=['other'],
            post_subject=post_subject,
            post_content=post_content,
            is_announcement=post.get('is_announcement', 0),
            bypass_email=post.get('bypass_email', 0),
            anonymous=False
        )
    except Exception:
        logger.exception('Exception')

logger.info('Done')
