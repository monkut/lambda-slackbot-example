import os
from typing import BinaryIO

from slackclient import SlackClient

CHANNEL_NAME = os.getenv('SLACK_CHANNEL', 'random')
SLACK_TOKEN = os.getenv('SLACK_API_TOKEN', None)
SLACK_BOT_NAME = os.getenv('SLACK_BOT_NAME', 'tobor')
SLACK_BOT_ICONURL = os.getenv(
    'SLACK_BOT_ICONURL',
    'https://web.archive.org/web/20170211223559if_/http://media-cache-ec0.pinimg.com/originals/64/7c/1f/647c1fc8eb682e974ab698a4814f508c.jpg'
)
DEFAULT_TEST_MESSAGE = ":fire: :fire: Tobor Rules :fire: :fire:"


class SlackError(Exception):
    pass


class SlackChannelError(Exception):
    pass


if not SLACK_TOKEN:
    raise SlackError('"SLACK_API_TOKEN" *required* environment variable not set!')


class SlackPostManager:

    def __init__(self, token: str = SLACK_TOKEN):
        self.sc = SlackClient(token)

    def _get_channel_id(self, channel_name: str) -> str:
        """
        Channels are referenced in the API by ID,
        This makes an API call to determine the given channel_name's id.
        """
        # get channel id for channel name
        channel_id = None
        channel_query_response = self.sc.api_call('channels.list',
                                                  exclude_archived=True)
        for channel_info in channel_query_response['channels']:
            if channel_info['name'] == channel_name:
                channel_id = channel_info['id']
                break
        if not channel_id:
            raise SlackChannelError(f'"{channel_name}" not found!')

        return channel_id

    def post_message_to_channel(self, channel_name: str = CHANNEL_NAME, message: str = DEFAULT_TEST_MESSAGE):
        """
        Posts the given 'message' to the channel
        """
        channel_id = self._get_channel_id(channel_name)
        self.sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            username=SLACK_BOT_NAME,
            icon_url=SLACK_BOT_ICONURL,
            text=message
        )

    def post_image_to_channel(self, channel_name: str, image_object: BinaryIO, title: str = 'Test Upload'):
        """
        Post an image to a channel
        """
        channel_id = self._get_channel_id(channel_name)

        self.sc.api_call(
            "files.upload",
            channels=channel_id,
            file=image_object.read(),
            title=title,
        )
