import sys
import logging
import datetime
import json
import urllib.request

from .managers import SlackPostManager

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(name)s) %(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)


def post_random_quote(event, context) -> None:
    # get random quote
    url = 'http://quotes.rest/qod.json?category=inspire'
    quote_json = urllib.request.urlopen(url).read().decode('utf8')
    quotes = json.loads(quote_json)
    quote_data = quotes['contents']['quotes'][0]
    quote_message = f'{quote_data["quote"]} -- {quote_data["author"]}'

    logger.info('posting image to slack...')
    slack = SlackPostManager()
    slack.post_message_to_channel(channel_name='random', message=quote_message)
    logger.info('posted!')
