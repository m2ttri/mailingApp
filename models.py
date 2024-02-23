from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Mailing(Base):
    __tablename__ = 'mailing'

    id = Column(Integer, primary_key=True, index=True)
    message_text = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    filter_criteria = Column(JSON)

    messages = relationship("Message", back_populates="mailing")


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String)
    mobile_operator_code = Column(String)
    tag = Column(String)
    timezone = Column(String)

    messages = relationship("Message", back_populates="client")


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    status = Column(String)
    mailing_id = Column(Integer, ForeignKey('mailing.id'))
    client_id = Column(Integer, ForeignKey('client.id'))

    mailing = relationship("Mailing", back_populates="messages")
    client = relationship("Client", back_populates="messages")
