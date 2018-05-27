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


class GMMessage:

    def __init__(self, group_id):
        self.group_id = group_id
        self.endpoint = f'https://api.groupme.com/v3/groups/{group_id}/messages?token={GM_API_TOKEN}&limit=100'
        self.messages_data = []
        self.last_message_id = None
        self.db_session = get_session()

    def pull_messages(self, before_id=None):
        try:
            if before_id:
                logger.info(f"Before ID: {before_id}")
                endpoint = f'{self.endpoint}&before_id={before_id}'
            else:
                endpoint = self.endpoint
            logger.info(f"Endpoint: {endpoint}")
            r = requests.get(endpoint)
            status_code = r.status_code
            if status_code == 304:
                return status_code
            self.messages_data = r.json()['response']['messages']
        except Exception as e:
            logger.error("Error pulling messages data")
            logger.error(f"Group ID: {self.group_id}")
            logger.error(f"After ID: {before_id}")
            logger.error(self.endpoint)
            logger.error(f"Request status code: {r.status_code}")
            logger.error(f"Request response: {r.text}")
            logger.error(e)
            raise
        if status_code == 200:
            return status_code
        else:
            raise Exception(f"Bad status code: {r.status_code}, {r.text}")

    def store_messages(self):
        for message_dict in self.messages_data:
            id = message_dict.get('id')
            sender_id = message_dict.get('sender_id')
            user_id = message_dict.get('user_id')
            sender_name = message_dict.get('name')
            favorite_count = len(message_dict.get('favorited_by'))
            created_at = message_dict.get('created_at')
            text = message_dict.get('text')

            attachment_num = 1
            for attachment_dict in message_dict.get('attachments'):
                type = attachment_dict.get('type')
                attachment_url = attachment_dict.get('url', None)
                attachment = Attachment(message_id=id, attachment_num=attachment_num, type=type,
                                        attachment_url=attachment_url)
                try:
                    self.db_session.add(attachment)
                except Exception as e:
                    logger.error("Unable to insert into database")
                    raise
                finally:
                    self.db_session.close()
                attachment_num += 1

            message = Message()
            message.id = id
            message.sender_id = sender_id
            message.user_id = user_id
            message.sender_name = sender_name
            message.favorite_count = favorite_count
            message.group_id = self.group_id
            message.created_at = created_at
            message.text = text

            try:
                self.db_session.add(message)
                self.db_session.commit()
            except Exception as e:
                logger.error("Unable to insert into database")
                raise
            finally:
                self.db_session.close()
            self.last_message_id = id

    def message_runner(self):
        i = 0
        while True:
            logger.info(f"Runnning iteration {i} of message puller")
            status_code = self.pull_messages(self.last_message_id)
            if status_code == 304:
                break
            self.store_messages()
            i += 1





if __name__ == '__main__':
    # create_database()

    # get all groups and members
    # g = GMGroup()
    # g.group_runner()

    # get all messages for one group
    g_message = GMMessage(13989673)
    g_message.message_runner()
