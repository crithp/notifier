"""
    Chris Thornton 2022-05-16
"""


class Config:
    def __init__(self, environment):
        # Internal
        self.environment = environment

        # Basic
        self.company_name = 'Test Company'

        # API configuration
        self.api_base = 'https://interview-assessment-1.realmdigital.co.za'

        # Testing
        # Set this if you want to try a particular date (string - 'YYYY-MM-DD')
        self.hard_coded_date = None  # '2022-05-16'

        # Email configuration
        self.email_enabled = False  # Enable when proper mail credentials provided

        self.login_email = 'test@example.com'
        self.login_port = 587
        self.login_password = 'WTmRX92Pn3mJeanz'  # Can be stored in an encrypted key vault for more advanced apps

        self.from_email = 'test@example.com'
        self.default_to_mail = 'christhornton@live.co.za'

