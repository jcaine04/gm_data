from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class Group(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(75))
    description = Column(String(255))


class Member(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    nickname = Column(String(100))


class Message(Base):
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    user_id = Column(Integer)
    sender_name = Column(String(100))
    favorite_count = Column(Integer)
    group_id = Column(Integer)

class Attachment(Base):
    message_id = Column(Integer)
    attachment_num = Column(Integer)
    type = Column(String(25))
    attachment_text = Column(Text)
