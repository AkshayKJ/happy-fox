import json
from datetime import datetime
from email_processor.models.constants import *

class Rule:
    """Class to represent rules"""
    def __init__(self, collection_predicate, conditions, actions):
        """Initialize the rule."""
        self.collection_predicate = collection_predicate
        self.conditions = conditions
        self.actions = actions

    @classmethod
    def from_dict(cls, data):
        """Create a rule from a dictionary."""
        if not all(key in data for key in RULE_KEYS):
            raise ValueError(f"Some fields are missing in the rule, expected fields are {', '.join(RULE_KEYS)}")

        collection_predicate = data[RULE_KEY_COLLECTION_PREDICATE]
        conditions = data[RULE_KEY_CONDITIONS]
        actions = data[RULE_KEY_ACTIONS]

        cls.validate_collection_predicate(collection_predicate)
        cls.validate_conditions(conditions)
        cls.validate_actions(actions)

        return cls(collection_predicate, conditions, actions)

    @classmethod
    def validate_collection_predicate(cls, collection_predicate):
        """Validate the collection predicate."""
        if collection_predicate not in RULE_COLLECTION_PREDICATES:
            raise ValueError(f"Collection predicate must be one of {', '.join(RULE_COLLECTION_PREDICATES)}")

    @classmethod
    def validate_conditions(cls, conditions):
        """Validate the conditions."""
        for condition in conditions:
            if not all(key in condition for key in RULE_CONDITION_KEYS):
                raise ValueError(f"Fields missing in the condition. Expected fields are {', '.join(RULE_CONDITION_KEYS)}")

            if condition[RULE_CONDITION_KEY_FIELD] not in RULE_FIELDS:
                raise ValueError(f"Invalid field in the condition. Allowed fields are {', '.join(RULE_FIELDS)}")

            if condition[RULE_CONDITION_KEY_FIELD] == RULE_FIELD_RECEIVED_DATE:
                if condition[RULE_CONDITION_KEY_PREDICATE] not in RULE_RECEIVED_DATE_PREDICATES:
                    raise ValueError(f"Invalid predicate for the received_date field. Allowed predicates are {', '.join(RULE_RECEIVED_DATE_PREDICATES)}")
                else:
                    try:
                        datetime.strptime(condition[RULE_CONDITION_KEY_VALUE], DATETIME_FORMAT)
                    except ValueError:
                        raise ValueError(f"Invalid date format in the condition. Accepted format is '{DATETIME_FORMAT}'")
            elif condition[RULE_CONDITION_KEY_PREDICATE] not in RULE_STRING_FIELDS_PREDICATES:
                raise ValueError(f"Invalid predicate for the field. Allowed predicates are {', '.join(RULE_STRING_FIELDS_PREDICATES)}")

    @classmethod        
    def validate_actions(cls, actions):
        """Validate the actions."""
        for action in actions:
            if action not in RULE_ACTIONS:
                raise ValueError(f"Invalid action. Allowed actions are {', '.join(RULE_ACTIONS)}")

    def __repr__(self):
        """Return the string representation of the rule."""
        return f"Rule(collection_predicate={self.collection_predicate}, conditions={self.conditions}, actions={self.actions})"
