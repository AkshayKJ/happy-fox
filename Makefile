PROJECT=EmailProcessor

.PHONY: env init create-db fetch-emails process-emails

env:
	@echo "Initializing environment..."
	export PYTHONPATH=$PYTHONPATH:$(PWD)

init: env
	@echo "Initializing $(PROJECT)..."
	pip3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt

create-db:
	@echo "Creating database..."
	python3 email_processor/models/emails.py

fetch-emails:
	@echo "Fetching emails..."
	python3 email_processor/service/fetch_emails.py

process-emails:
	@echo "Processing emails based on rules..."
	python3 email_processor/service/process_rules.py

echo-run-email-processor:
	@echo "Running email processor..."

run-email-processor: echo-run-email-processor init create-db fetch-emails process-emails
