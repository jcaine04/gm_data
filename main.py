import logging
import os

import requests

from data import Group, Member, Message, Attachment
from data import get_session, create_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GM_API_TOKEN = os.environ.get('GM_API_TOKEN')


class GMGroup:

    def __init__(self):
        self.endpoint = f'https://api.groupme.com/v3/groups?token={GM_API_TOKEN}'
        self.groups_list = []
        self.db_session = get_session()

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
            self.db_session.add(group)
            self.db_session.commit()

    def store_members(self):
        for group_dict in self.groups_list:
            members = group_dict.get('members')
            group_id = group_dict.get('id')
            for members_dict in members:
                id = members_dict.get('id')
                user_id = members_dict.get('user_id')
                nickname = members_dict.get('nickname')
                member = Member(id=id, user_id=user_id, nickname=nickname, group_id=group_id)
                self.db_session.add(member)
                self.db_session.commit()

    def group_runner(self):
        logger.info("Pulling groups from the api")
        self.pull_groups()
        logger.info("Storing groups in database")
        self.store_groups()
        logger.info("Storing members from each group")
        self.store_members()


class GMMember:

    def __init__(self):
        self.endpoint = self.endpoint = f'https://api.groupme.com/v3/groups?token={GM_API_TOKEN}'



if __name__ == '__main__':
    g = GMGroup()
    g.group_runner()
