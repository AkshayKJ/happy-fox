import base64
import email.utils
import os.path
import pickle
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from email_processor.models.emails import insert_email
from typing import List, Dict, Any, Optional
import email_processor.service.constants as constants

# List to store email messages
emails = []


def get_messages(
    service: Any,
    message_ids: List[str],
    user_id: Optional[str]=constants.DEFAULT_GMAIL_USER_ID
) -> None:
    """
    Get email messages in batches.
    Parameters:
        service: googleapiclient.discovery.Resource - Gmail API service object
        message_ids: List[str] - list of email message IDs
        user_id: str - user's email address
    """
    for i in range(0, len(message_ids), 50):
        batch = service.new_batch_http_request(callback=callback)
        for message_id in message_ids[i:i+50]:
            batch.add(service.users().messages().get(
                userId=user_id, id=message_id))
        try:
            batch.execute()
        except HttpError as error:
            print(
                f'Error occured while requesting email messages in batches: {error}')
            raise error


def callback(request_id, response, exception):
    if exception is not None:
        print(f'Error occured while processing batch request: {exception}')
    else:
        emails.append(response)


def get_service() -> Any:
    """
    Shows basic usage of the Gmail API
    Returns authenticated Gmail API service
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                constants.CREDENTIALS_PATH, constants.SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_user_email(service: Any, user_id: Optional[str]=constants.DEFAULT_GMAIL_USER_ID) -> str:
    """
    Get user's email address.
    Parameters:
        service: googleapiclient.discovery.Resource - Gmail API service object
        user_id: str - user's email address
    """
    try:
        user_info = service.users().getProfile(userId=user_id).execute()
        return user_info['emailAddress']
    except HttpError as error:
        print(f"Error occured fetching user's email address: {error}")
        raise error


def list_messages(service: Any, user_id: Optional[str]=constants.DEFAULT_GMAIL_USER_ID) -> List[str]:
    """
    List all Messages of the user's mailbox, handling pagination.
    Parameters:
        service: googleapiclient.discovery.Resource - Gmail API service object
        user_id: str - user's email address
    """
    try:
        next_page_token, messages = None, []

        while len(messages) < constants.MAX_EMAILS_TO_FETCH:

            maxResultSize = constants.MAX_EMAILS_TO_FETCH
            if constants.MAX_EMAILS_TO_FETCH > constants.LIST_EMAILS_PAGINATION_MAX_SIZE:
                maxResultSize = constants.LIST_EMAILS_PAGINATION_MAX_SIZE

            response = service.users().messages().list(
                userId=user_id,
                pageToken=next_page_token,
                maxResults=maxResultSize,
                includeSpamTrash=constants.LIST_EMAILS_INCLUDE_SPAM_TRASH_EMAILS
            ).execute()
            print(response)
            messages.extend(response.get('messages', []))

            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break

        if not messages:
            print("No messages found.")
        else:
            print(f"Total messages fetched: {len(messages)}")

        messages = [message['id'] for message in messages]
        return messages

    except HttpError as error:
        print(f'An error occurred while fetching emails: {error}')
        raise error


def process_email_body(message_body_parts: List[Dict[str, Any]]) -> str:
    """
    Process email body.
    Parameters:
        message_body_parts: List[Dict[str, Any]] - list of email body parts
    """
    message_body = []
    for part in message_body_parts:
        if part['mimeType'] == 'text/plain':
            decoded_body = base64.urlsafe_b64decode(
                part['body']['data'] + '===').decode('utf-8', errors='ignore')
            message_body.append(re.sub(r'\s+', ' ', decoded_body))
    return ", ".join(message_body)


def insert_emails(to_email: str) -> None:
    """
    Insert email messages into the database.
    Parameters:
        to_email: str - email address of the recipient
    """
    for message in emails:
        message_id = message['id']
        to_address = to_email
        body = process_email_body(message['payload']['parts'])

        from_address = ", ".join(
            [header['value'] for header in message['payload']
                ['headers'] if header['name'] == 'From']
        )

        subject = ", ".join(
            [header['value'] for header in message['payload']
                ['headers'] if header['name'] == 'Subject']
        )

        received_date = email.utils.parsedate_to_datetime(
            [header['value'] for header in message['payload']
                ['headers'] if header['name'] == 'Date'][0]
        )

        insert_email(
            message_id=message_id,
            from_address=from_address,
            to_address=to_address,
            subject=subject,
            received_date=received_date,
            body=body
        )


def fetch_emails() -> None:
    """Fetch emails from Gmail and insert them into the database."""
    service = get_service()
    user_email = get_user_email(service)
    message_ids = list_messages(service)
    get_messages(service, message_ids)
    insert_emails(user_email)


if __name__ == '__main__':
    fetch_emails()
