from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from email_processor.models.constants import DATABASE_URL
from email_processor.models.query import fetch_email_ids


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



DB_ENGINE = create_engine(DATABASE_URL, echo=True)
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def insert_email(message_id, from_address, to_address, subject, received_date, body):
    """Insert email message into the database."""
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
        print(f"An error occurred while inserting emails in db: {e}")
        session.rollback()
    finally:
        session.close()


def get_email_ids_for_rules(rule):
    """Get email IDs for the given rule."""
    session = DB_SESSION()
    email_ids = fetch_email_ids(session, EmailMessage, rule)
    return email_ids


def create_database():
    """Create the database."""
    BASE.metadata.create_all(DB_ENGINE)


if __name__ == "__main__":
    create_database()
