import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text


engine = create_engine(os.environ.get('SQLITE_DB_PATH'), echo=False)
Base = declarative_base(engine)


def create_database():
    Base.metadata.create_all()

def get_session():
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(String, primary_key=True)
    name = Column(String(75))
    description = Column(String(255))


class Member(Base):
    __tablename__ = 'members'
    id = Column(String, primary_key=True)
    user_id = Column(String)
    nickname = Column(String(100))
    group_id = Column(String)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True)
    sender_id = Column(String)
    user_id = Column(String)
    sender_name = Column(String(100))
    favorite_count = Column(Integer)
    group_id = Column(String)
    created_at = Column(Integer)
    text = Column(Text)

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)
    attachment_num = Column(Integer)
    type = Column(String(25))
    attachment_url = Column(String)