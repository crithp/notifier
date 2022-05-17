# Automated mailer

## Installation
- Simply place the program files anywhere in a desired location on your server
- Python 3.9+ is required to execute this program
- Review configuration variables in Config.py and set as needed
- If email functionality is required, set email variables then set email_enabled to True

## Execution
- execute "python3 main.py" while in the project file directory from an administrative terminal
- Output for the application's actions will appear in the terminal

## Testing
- To put the service into development mode, simply add the environment variable "ENVIRONMENT=dev"
- Once in development mode, you can edit dummy_people.json and dummy_exception.json in /test as you wish to test components
- To test as if it were a particular date, set the hard_coded_date variable in the conf to the desired date