from datetime import datetime
from email_processor.models.constants import *


def fetch_email_ids(db_session, email_table, rule):
    """Fetch email IDs from the database based on the rule."""
    email_ids = []
    try:
        query = db_session.query(email_table.message_id)
        if rule.collection_predicate == RULE_COLLECTION_PREDICATE_ALL:
            for condition in rule.conditions:
                field = condition[RULE_CONDITION_KEY_FIELD]
                predicate = condition[RULE_CONDITION_KEY_PREDICATE]
                value = condition[RULE_CONDITION_KEY_VALUE]
                if field == RULE_FIELD_RECEIVED_DATE:
                    datetime_val = datetime.strptime(condition[RULE_CONDITION_KEY_VALUE], DATETIME_FORMAT)
                    if predicate == RULE_PREDICATE_GREATER_THAN:
                        query = query.filter(email_table.received_date > datetime_val)
                    elif predicate == RULE_PREDICATE_LESSER_THAN:
                        query = query.filter(email_table.received_date < datetime_val)
                    elif predicate == RULE_PREDICATE_GREATER_THAN_EQUAL_TO:
                        query = query.filter(email_table.received_date >= datetime_val)
                    elif predicate == RULE_PREDICATE_LESSER_THAN_EQUAL_TO:
                        query = query.filter(email_table.received_date <= datetime_val)
                elif field in RULE_STRING_FIELDS:
                    if predicate == RULE_PREDICATE_CONTAINS:
                        query = query.filter(getattr(email_table, field).contains(value))
                    elif predicate == RULE_PREDICATE_DOES_NOT_CONTAIN:
                        query = query.filter(~getattr(email_table, field).contains(value))
            email_ids = [email.message_id for email in query.all()]
        
        elif rule.collection_predicate == RULE_COLLECTION_PREDICATE_ANY:
            for condition in rule.conditions:
                field = condition[RULE_CONDITION_KEY_FIELD]
                predicate = condition[RULE_CONDITION_KEY_PREDICATE]
                value = condition[RULE_CONDITION_KEY_VALUE]
                if field == RULE_FIELD_RECEIVED_DATE:
                    if predicate == RULE_PREDICATE_GREATER_THAN:
                        query = query.filter(email_table.received_date > value)
                    elif predicate == RULE_PREDICATE_LESSER_THAN:
                        query = query.filter(email_table.received_date < value)
                    elif predicate == RULE_PREDICATE_GREATER_THAN_EQUAL_TO:
                        query = query.filter(email_table.received_date >= value)
                    elif predicate == RULE_PREDICATE_LESSER_THAN_EQUAL_TO:
                        query = query.filter(email_table.received_date <= value)
                elif field in RULE_STRING_FIELDS:
                    if predicate == RULE_PREDICATE_CONTAINS:
                        query = query.filter(getattr(email_table, field).contains(value))
                    elif predicate == RULE_PREDICATE_DOES_NOT_CONTAIN:
                        query = query.filter(~getattr(email_table, field).contains(value))
                email_ids.extend([email.message_id for email in query.all()])
    
    except Exception as e:
        print(f"An error occurred while reading emails from db: {e}")
    finally:
        db_session.close()
        print(email_ids)
        return email_ids

