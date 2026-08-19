# ThingsBoard Test Automation

Automation tests for the ThingsBoard telemetry dashboard.

## Tech Used

- Python
- Pytest
- Playwright
- Requests
- python-dotenv

## Setup

Install the required packages:


pip install -r requirements.txt
playwright install chromium

Create a .env file in the project root:

THINGSBOARD_URL=<url>
THINGSBOARD_USERNAME=<username>
THINGSBOARD_PASSWORD=<password>
DEVICE_TOKEN=<device-token>


Keep the .env file local and do not commit it.

## Running the telemetry

The telemetry script sends temperature, humidity and power consumption values to the device every 5 seconds.


python test_data/send_telemetry.py

## Running the tests

UI tests:

python -m pytest tests/test_dashboard_ui.py -s -v

API tests:


python -m pytest tests/test_api_telemetry.py -s -v

## What is covered

- Login and dashboard access
- Dashboard telemetry widgets
- Temperature, humidity and power values
- Real-time telemetry updates
- API authentication and telemetry query
- API response and value validation
- Retry when telemetry is not immediately available
- Device active/inactive behavior
- Telemetry stop and recovery scenarios

## Test Results

Test cases and defect details are available in:

- test_cases.xlsx
- bug_report.xlsx

Screenshots and other test evidence are in the 'evidence' folder.
