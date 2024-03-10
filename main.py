#!/usr/bin/env python3

__author__ = "Akshay Kumar"
__credits__ = ["Akshay Kumar"]
__email__ = "mailatakshaykumar@gmail.com"
__status__ = "Development"
__version__ = "0.0.1"

from email_processor.models.emails import create_database
from email_processor.service.fetch_emails import fetch_emails
from email_processor.service.process_rules import process_emails_for_rule_actions


def main():
    create_database()
    fetch_emails()
    process_emails_for_rule_actions()


if __name__ == "__main__":
    main()
