# Replace the connection string with your actual database credentials
import os


SQLALCHEMY_ECHO_MODE = os.getenv("SQLALCHEMY_ECHO_MODE")
if SQLALCHEMY_ECHO_MODE == "True":
    SQLALCHEMY_ECHO_MODE = True
elif SQLALCHEMY_ECHO_MODE == "debug":
    SQLALCHEMY_ECHO_MODE = "debug"
else:
    SQLALCHEMY_ECHO_MODE = False

DATABASE_URL = "sqlite:///email.db"
DATETIME_FORMAT = '%d-%m-%Y'
RULE_ACTION_MOVE_TO_FOLDER = "move_to_folder"
RULE_ACTION_MARK_AS_READ = "mark_as_read"
RULE_ACTIONS = [RULE_ACTION_MOVE_TO_FOLDER, RULE_ACTION_MARK_AS_READ]
RULE_KEY_COLLECTION_PREDICATE = 'collection_predicate'
RULE_COLLECTION_PREDICATE_ALL = 'All'
RULE_COLLECTION_PREDICATE_ANY = 'Any'
RULE_COLLECTION_PREDICATES = [RULE_COLLECTION_PREDICATE_ALL, RULE_COLLECTION_PREDICATE_ANY]
RULE_KEY_CONDITIONS = 'conditions'
RULE_KEY_ACTIONS = 'actions'
RULE_KEYS = [RULE_KEY_COLLECTION_PREDICATE, RULE_KEY_CONDITIONS, RULE_KEY_ACTIONS]
RULE_CONDITION_KEY_FIELD = 'field'
RULE_CONDITION_KEY_PREDICATE = 'predicate'
RULE_CONDITION_KEY_VALUE = 'value'
RULE_CONDITION_KEYS = [
    RULE_CONDITION_KEY_FIELD,
    RULE_CONDITION_KEY_PREDICATE,
    RULE_CONDITION_KEY_VALUE
]
RULE_FIELD_FROM_ADDRESS = 'from_address'
RULE_FIELD_TO_ADDRESS = 'to_address'
RULE_FIELD_SUBJECT = 'subject'
RULE_FIELD_RECEIVED_DATE = 'received_date'
RULE_FIELD_BODY = 'body'
RULE_FIELDS = [RULE_FIELD_FROM_ADDRESS, RULE_FIELD_TO_ADDRESS, RULE_FIELD_SUBJECT, RULE_FIELD_RECEIVED_DATE, RULE_FIELD_BODY]
RULE_STRING_FIELDS = [RULE_FIELD_FROM_ADDRESS, RULE_FIELD_TO_ADDRESS, RULE_FIELD_SUBJECT, RULE_FIELD_BODY]
RULE_PREDICATE_CONTAINS = 'contains'
RULE_PREDICATE_DOES_NOT_CONTAIN = 'does not contain'
RULE_PREDICATE_GREATER_THAN = 'gt'
RULE_PREDICATE_GREATER_THAN_EQUAL_TO = 'gte'
RULE_PREDICATE_LESSER_THAN = 'lt'
RULE_PREDICATE_LESSER_THAN_EQUAL_TO = 'lte'
RULE_STRING_FIELDS_PREDICATES = [RULE_PREDICATE_CONTAINS, RULE_PREDICATE_DOES_NOT_CONTAIN]
RULE_RECEIVED_DATE_PREDICATES = [
    RULE_PREDICATE_GREATER_THAN,
    RULE_PREDICATE_GREATER_THAN_EQUAL_TO,
    RULE_PREDICATE_LESSER_THAN,
    RULE_PREDICATE_LESSER_THAN_EQUAL_TO
]