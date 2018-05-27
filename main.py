import logging
import os

import requests

from data import Group, Member, Message, Attachment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GM_API_TOKEN = os.environ.get('GM_API_TOKEN')


class GM_Group:

    def __init__(self):
        self.endpoint = f'https://api.groupme.com/v3/groups?token={GM_API_TOKEN}'
        self.groups_list = []

    def pull_groups(self):
        try:
            r = requests.get(self.endpoint)
        except Exception as e:
            logger.error("Problem pulling from GroupMe API")
            logger.error(e)
            raise

        self.groups_list = r.json()['response']

    def store_groups(self):
        for group_dict in self.groups_list:
            id = group_dict.get('id')
            name = group_dict.get('name')
            description = group_dict.get('description')

            group = Group(id=id, name=name, description=description)
            #TODO: Need to add code to store this stuff


