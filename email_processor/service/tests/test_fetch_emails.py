import unittest
from unittest.mock import MagicMock, Mock, patch
from email_processor.service import fetch_emails
from googleapiclient.errors import HttpError

class TestFetchEmails(unittest.TestCase):
    def test_get_user_email_when_profile_call_is_successful(self):
        # Mock the service object
        service = MagicMock()
        service.users().getProfile().execute.return_value = {'emailAddress': 'test@example.com'}

        # Call the function
        user_email = fetch_emails.get_user_email(service)

        # Assert that the service.users().getProfile().execute() method was called
        service.users().getProfile().execute.assert_called_once()

        # Assert that the returned user_email is correct
        self.assertEqual(user_email, 'test@example.com')

    def test_get_user_email_when_profile_call_fails(self):
        # Mock the service object
        service = MagicMock()
        service.users().getProfile().execute.side_effect = HttpError(Mock(status=500), b'Internal Server Error')

        # Call the function
        with self.assertRaises(HttpError):
            fetch_emails.get_user_email(service)

        # Assert that the service.users().getProfile().execute() method was called
        service.users().getProfile().execute.assert_called_once()
    
    def test_list_messages_when_messages_are_fetched(self):
        # Mock the service object
        service = MagicMock()
        service.users().messages().list().execute.side_effect = [
            {'messages': [{'id': '1'}, {'id': '2'}], 'nextPageToken': 'token'},
            {'messages': [{'id': '3'}, {'id': '4'}]}
        ]

        # Call the function
        messages = fetch_emails.list_messages(service)

        # Assert that the service.users().messages().list().execute() method was called twice
        self.assertEqual(service.users().messages().list().execute.call_count, 2)

        # Assert that the returned messages are correct
        self.assertEqual(messages, ['1', '2', '3', '4'])
    
    def test_list_messages_when_messages_call_fails(self):
        # Mock the service object
        service = MagicMock()
        service.users().messages().list().execute.side_effect = HttpError(Mock(status=500), b'Internal Server Error')
        with self.assertRaises(HttpError):
            fetch_emails.list_messages(service)
        
        # Assert that the service.users().getProfile().execute() method was called
        service.users().messages().list().execute.assert_called_once()
    
    def test_list_messages_when_no_messages_are_fetched(self):
        # Mock the service object
        service = MagicMock()
        service.users().messages().list().execute.return_value = {}

        # Call the function
        messages = fetch_emails.list_messages(service)

        # Assert that the service.users().messages().list().execute() method was called
        service.users().messages().list().execute.assert_called_once()

        # Assert that the returned messages are correct
        self.assertEqual(messages, [])
    
    def test_process_email_body_when_body_is_fetched(self):
        # Mock the message_body_parts
        message_body_parts = [
            {'mimeType': 'text/plain', 'body': {'data': 'VGhpcyBpcyBhIHRlc3QgYm9keSB0byBkYXRhCg=='}}
        ]

        # Call the function
        body = fetch_emails.process_email_body(message_body_parts)

        # Assert that the returned body is correct
        self.assertEqual(body, 'This is a test body to data ')

    def test_process_email_body_when_body_is_not_fetched(self):
        # Mock the message_body_parts
        message_body_parts = []

        # Call the function
        body = fetch_emails.process_email_body(message_body_parts)

        # Assert that the returned body is correct
        self.assertEqual(body, '')


if __name__ == '__main__':
    unittest.main()
