import unittest
from unittest.mock import MagicMock, Mock, patch

from googleapiclient.errors import HttpError
from email_processor.models.rules import Rule
from email_processor.service.process_rules import (
    get_label_id,
    perform_rule_actions,
    process_emails_for_rule_actions,
)


class TestProcessRules(unittest.TestCase):

    def test_get_label_id(self):
        # Mock the service object
        service = MagicMock()
        service.users().labels().list().execute.return_value = {
            'labels': [
                {'id': 'label1', 'name': 'Label1'},
                {'id': 'label2', 'name': 'Label2'},
            ]
        }

        # Call the function
        label_id = get_label_id(service, 'Label2')

        # Assert that the service.users().labels().list().execute() method was called
        service.users().labels().list().execute.assert_called_once()

        # Assert that the returned label_id is correct
        self.assertEqual(label_id, 'label2')

    @patch('email_processor.service.process_rules.get_label_id')
    def test_perform_rule_actions_on_success(self, mock_get_label_id):
        # Mock the service object
        service = MagicMock()
        mock_get_label_id.return_value = 'label2'
        service.users().labels().list(userId='me').execute.return_value = 'label2'
        service.users().messages().modify.return_value.execute.return_value = {}

        # Call the function
        rule = {
            "collection_predicate": "All",
            "conditions": [
                {
                    "field": "from_address",
                    "predicate": "contains",
                    "value": "bytebytego@substack.com"
                },
                {
                    "field": "received_date",
                    "predicate": "gt",
                    "value": "08-03-2024"
                }
            ],
            "actions": {
                "mark_as_read": False,
                "move_to_folder": "label2"
            }
        }
        rule = Rule.from_dict(rule)
        perform_rule_actions(service, ['1', '2'], rule, 'me')
    

if __name__ == '__main__':
    unittest.main()
