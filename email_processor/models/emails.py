import logging
from typing import Any
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from email_processor.models.constants import DATABASE_URL, SQLALCHEMY_ECHO_MODE
from email_processor.models.query import fetch_email_ids
from email_processor.models.rules import Rule


BASE = declarative_base()


class EmailMessage(BASE):
    """Class to represent email messages."""
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    message_id = Column(String, unique=True, nullable=False)
    from_address = Column(String)
    to_address = Column(String)
    subject = Column(String)
    received_date = Column(DateTime)
    body = Column(Text)


DB_ENGINE = create_engine(DATABASE_URL, echo=SQLALCHEMY_ECHO_MODE)
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def insert_email(message_id: str, from_address: str, to_address: str, subject: str, received_date: DateTime, body: str):
    """
    Insert email message into the database.
    Parameters:
        message_id: str - message ID
        from_address: str - sender's email address
        to_address: str - recipient's email address
        subject: str - email subject
        received_date: DateTime - date and time when the email was received
        body: str - email body
    """
    session = DB_SESSION()
    email_message = EmailMessage(
        message_id=message_id,
        from_address=from_address,
        to_address=to_address,
        subject=subject,
        received_date=received_date,
        body=body
    )
    session.add(email_message)
    try:
        session.commit()
    except Exception as e:
        logging.error(f"An error occurred while inserting emails in db: {e}")
        session.rollback()
    finally:
        session.close()


def get_email_ids_for_rules(rule: Rule):
    """
    Get email IDs for the given rule.
    Parameters:
        rule: Rule - rule object
    """
    session = DB_SESSION()
    email_ids = fetch_email_ids(session, EmailMessage, rule)
    return email_ids


def create_database():
    """Create the database."""
    BASE.metadata.create_all(DB_ENGINE)


if __name__ == "__main__":
    create_database()
