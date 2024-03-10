PROJECT=EmailProcessor

export PYTHONPATH=$${PYTHONPATH}:$(PWD)

.PHONY: init create-db fetch-emails process-emails

create-venv:
	@echo "Initializing $(PROJECT)..."
	python3 -m venv venv

init: create-venv
	@echo "Activating virtual environment & installing deps..."
	source venv/bin/activate && pip3 install -r requirements.txt

create-db:
	@echo "Creating database..."
	source venv/bin/activate && python3 email_processor/models/emails.py

fetch-emails:
	@echo "Fetching emails..."
	source venv/bin/activate && python3 email_processor/service/fetch_emails.py

process-emails:
	@echo "Processing emails based on rules..."
	source venv/bin/activate && python3 email_processor/service/process_rules.py

run-email-processor: init
	@echo "Running email processor..."
	source venv/bin/activate && python3 __main__.py
