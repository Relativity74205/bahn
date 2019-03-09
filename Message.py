from sqlalchemy import Column, Integer, String, DateTime

from DatabaseConnection import Base


class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    trainstop_id = Column(String)
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
