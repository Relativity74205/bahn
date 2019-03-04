from sqlalchemy import Column, Integer, String, DateTime

import config.config as config
from DatabaseConnection import Base


class MessageIDs(Base):
    id = Column(Integer, primary_key=True)
    trainstop_id = Column(Integer)
    message_id = Column(Integer)

    def __init__(self, trainstop_id, message_id):
        self.trainstop_id = trainstop_id
        self.message_id = message_id


class Message(Base):
    message_id = Column(Integer, primary_key=True)
    message_type = Column(String)
    from_datetime = Column(DateTime)
    to_datetime = Column(DateTime)
    priority = Column(Integer)
    bahn_code = Column(Integer)
    internal_text = Column(String)
    external_text = Column(String)
    category = Column(String)
    external_category = Column(String)
    tstamp = Column(DateTime)
    owner = Column(String)
    external_link = Column(String)
    flag_deleted = Column(Integer)
    distributor_message = Column(String)
    trip_label = Column(String)

    def __init__(self):
        pass
