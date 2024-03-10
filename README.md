# Email Processor

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This project is a Python-based application designed to interact with the Gmail API. It fetches emails, processes them, and stores the information in a local database. The main functionality includes retrieving email messages in batches, parsing the emails, and storing the parsed data. The project uses SQLAlchemy for database interactions and the Google API client for Gmail interactions. It's designed with modularity and scalability in mind, allowing for easy expansion and modification.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## Prerequisites
1. Enable and add your Google Cloud Console Gmail API `credentials.json` in the repo directory. Necessary scope for the API creds: ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.labels']
2. Setup `rules.json` at `email_processor/service/rules.json`. Sample rules JSON present for reference.

## Installation

- Run `make init` to setup a virtual env and install requirements

## Usage

- Make use of available make tasks to run the scripts:
    1. Local Sqlalchemy DB Creation: `make create-db`. Utilize `SQLALCHEMY_ECHO_MODE` env var to set sqlalchemy logging level (True, False, debug).
    2. Fetch all emails: `make fetch-emails`. Note that `email_processor/service/constants.py` contains constants for configuring Gmail List Emails API desired size and pagination size.
    3. Process emails based on `rules.json`: `make fetch-emails`. Note that `email_processor/service/constants.py` contains constants for configuring Gmail Modify Email Labels API batch size.
    4. Run all of the above steps in a single task: `make run-email-processor`.

#### Note: Refer and utilize constants files for configurations

## Contributing

Not open for contribution at the moment.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- Email: mailatakshaykumar@gmail.com
- GitHub: [AkshayKJ](https://github.com/AkshayKJ)