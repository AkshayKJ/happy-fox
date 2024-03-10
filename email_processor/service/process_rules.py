import json
import logging
import requests
from typing import Any, List, Optional
from email_processor.models.constants import RULE_ACTION_MARK_AS_READ, RULE_ACTION_MOVE_TO_FOLDER
from email_processor.models.emails import get_email_ids_for_rules
from email_processor.models.rules import Rule
from email_processor.service.constants import DEFAULT_GMAIL_USER_ID, RULE_FILE_PATH, MODIFY_EMAILS_BATCH_SIZE
from email_processor.service.fetch_emails import get_service


def read_rules_from_json(file_path: Optional[str] = RULE_FILE_PATH) -> Rule:
    """
    Read rules from a JSON file.
    Parameters:
        file_path: str - path to the JSON file containing rules
    """
    with open(file_path, 'r') as file:
        rules_data = json.load(file)

    try:
        rules = Rule.from_dict(rules_data)
        return rules
    except ValueError as e:
        logging.error(f"Error processing rules: {str(e)}")
        raise e


def get_label_id(service: Any, folder_name: str) -> Optional[str]:
    """
    Get label ID for the given folder name.
    Parameters:
        service: googleapiclient.discovery.Resource - Gmail API service object
        folder_name: str - name of the folder
    """
    try:
        labels = service.users().labels().list(userId='me').execute()
        for label in labels['labels']:
            if label['name'] == folder_name:
                return label['id']
        return None
    except Exception as e:
        logging.error(f"Error getting label ID for folder: {str(e)}")
        return None


def perform_rule_actions(
    service: Any,
    email_ids: List[str],
    rules: Rule,
    user_id: Optional[str] = DEFAULT_GMAIL_USER_ID
) -> None:
    """
    Perform rule actions on emails using Gmail service for batch modification.
    Parameters:
        service: googleapiclient.discovery.Resource - Gmail API service object
        email_ids: list - list of email IDs
        rules: Rule - rule object
        user_id: str - user ID
    """
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

    logging.info(
        f"Performing rule actions: addLabelIds={addLabelIds}, removeLabelIds={removeLabelIds}")

    for batch in batches:
        # Perform batch modification using Gmail service
        batch_request = {
            "ids": [email_id for email_id in batch],
            "addLabelIds": addLabelIds,
            "removeLabelIds": removeLabelIds
        }
        try:
            service.users().messages().batchModify(
                userId=user_id, body=batch_request).execute()
            logging.info(f"Rule actions performed successfully for batch: {batch}")
        except requests.HTTPError as error:
            logging.error(
                f'Error occured while performing email actions in batches: {error}')
            raise error


def process_emails_for_rule_actions() -> None:
    """Process emails for the given rule actions."""
    service, rules = get_service(), read_rules_from_json()
    email_ids = get_email_ids_for_rules(rules)

    perform_rule_actions(service, email_ids, rules)


if __name__ == "__main__":
    process_emails_for_rule_actions()
