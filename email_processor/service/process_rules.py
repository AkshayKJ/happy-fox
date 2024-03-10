import json
import requests
from email_processor.models.constants import RULE_ACTION_MARK_AS_READ, RULE_ACTION_MOVE_TO_FOLDER
from email_processor.models.emails import get_email_ids_for_rules
from email_processor.models.rules import Rule
from email_processor.service.constants import DEFAULT_GMAIL_USER_ID, RULE_FILE_PATH, MODIFY_EMAILS_BATCH_SIZE
from email_processor.service.fetch_emails import get_service


def read_rules_from_json(file_path=RULE_FILE_PATH):
    """Read rules from a JSON file."""
    with open(file_path, 'r') as file:
        rules_data = json.load(file)

    try:
        rules = Rule.from_dict(rules_data)
        return rules
    except ValueError as e:
        print(f"Error processing rules: {str(e)}")
        raise e


def get_label_id(service, folder_name):
    """Get label ID for the given folder name."""
    try:
        labels = service.users().labels().list(userId='me').execute()
        for label in labels['labels']:
            if label['name'] == folder_name:
                return label['id']
        return None
    except Exception as e:
        print(f"Error getting label ID for folder: {str(e)}")
        return None


def perform_rule_actions(service, email_ids, rules, user_id=DEFAULT_GMAIL_USER_ID):
    """Perform rule actions on emails using Gmail service for batch modification."""
    # Split email ids into batches
    batches = [email_ids[i:i + MODIFY_EMAILS_BATCH_SIZE]
               for i in range(0, len(email_ids), MODIFY_EMAILS_BATCH_SIZE)]

    addLabelIds, removeLabelIds = [], []

    for action, value in rules.actions.items():
        if action == RULE_ACTION_MOVE_TO_FOLDER:
            folder_name = get_label_id(service, value)
            if folder_name:
                addLabelIds.append(folder_name)
            else:
                raise ValueError(f"Error: Label '{value}' not found.")
        elif action == RULE_ACTION_MARK_AS_READ:
            if value:
                removeLabelIds.append("UNREAD")
            else:
                addLabelIds.append("UNREAD")

    for batch in batches:
        # Perform batch modification using Gmail service
        batch_request = {
            "ids": [email_id for email_id in batch],
            "addLabelIds": addLabelIds,
            "removeLabelIds": removeLabelIds
        }
        print(batch_request)
        try:
            service.users().messages().batchModify(
                userId=user_id, body=batch_request).execute()
            print(f"Rule actions performed successfully for batch: {batch}")
        except requests.HTTPError as error:
            print(
                f'Error occured while performing email actions in batches: {error}')
            raise error


def process_emails_for_rule_actions():
    """Process emails for the given rule actions."""
    service, rules = get_service(), read_rules_from_json()
    email_ids = get_email_ids_for_rules(rules)

    perform_rule_actions(service, email_ids, rules)


if __name__ == "__main__":
    process_emails_for_rule_actions()