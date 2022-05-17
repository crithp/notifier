"""
    Chris Thornton 2022-05-16
"""
import re
import json
import ssl
import lib.shared_globals as shared_globals
from datetime import datetime, date
import urllib.request
from lib.sender import Sender


class BirthdaySender(Sender):
    def __init__(self, logger):
        super().__init__(logger)
        self.name = 'Birthday sender'

        self.curdate = None  # Instantiated on run, just so we don't waste time on calling the internal function

        # List of person ID and date of notification, without the date if the application ran for more than a year
        # than they wouldn't get more messages
        self.birthdays_notified = []

    def execute(self):
        # Don't execute this before everyone is in the office
        if datetime.now().hour < 9:
            return

        self.logger.debug('Executing birthday sender')

        if shared_globals.conf.hard_coded_date is None:
            self.curdate = datetime.now()
        else:
            # Can use this to hardcode the date and check
            self.curdate = datetime.strptime(shared_globals.conf.hard_coded_date, '%Y-%m-%d')

        birthday_people = self.fetch_birthdays()

        for person in birthday_people:
            # Relates to self.birthdays_notified, see comment in the __init__ function
            check_key = f"{person['id']}-{self.curdate.strftime('%Y-%m-%d')}"

            # Will only check if the person has an exception if they have a birthday, most efficient
            # this way, we only make another API call if necessary
            if self.has_birthday(person) \
                    and check_key not in self.birthdays_notified \
                    and not self.has_exception(person):
                # Now we know we can send the email
                self.logger.info(f"Sending birthday email to {person['id']}")
                success = self.send_email(*self.generate_email(person))  # Inherited from Sender class
                if success:  # Only mark this person off if the mail successfully went through
                    # Mark the person as completed so we don't mail them again, would preferably store this through
                    # the API but for the purposes of this demo we'll store this in memory
                    self.birthdays_notified.append(f"{person['id']}-{self.curdate.strftime('%Y-%m-%d')}")
                    self.logger.info(f"Successfully sent birthday email to {person['id']}")

    def fetch_birthdays(self):
        # If it's development, then use the dummy data
        if shared_globals.is_dev:
            with open('test/dummy_people.json', 'r+') as infile:
                return json.loads(infile.read())
        else:  # Fetch from API
            # Found that the API is using a self-signed cert, need to ignore this
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(shared_globals.conf.api_base + '/employees', context=ctx) as response:
                return json.loads(response.read())

            # API is down, return an empty list, not too much of a concern as the API may come back again today
            # Just log it so that someone can see
            self.logger.error("API is unavailable")
            return []

    def fetch_exceptions(self):
        # If it's development, then use the dummy data
        if shared_globals.is_dev:
            with open('test/dummy_exception.json', 'r+') as infile:
                return json.loads(infile.read())
        else:  # Fetch from API
            # Found that the API is using a self-signed cert, need to ignore this
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(shared_globals.conf.api_base + '/do-not-send-birthday-wishes', context=ctx) \
                    as response:
                return json.loads(response.read())

            # Unlike for fetching birthdays, the exceptions are critical, if it fails then crash
            self.logger.error("Could not fetch exception list")
            raise Exception("Could not fetch exception list")

    def has_birthday(self, person):
        # Just a basic regex to extract just the date
        for day in re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", person['dateOfBirth']):
            try:  # Dirty date could crash this
                bday = datetime.strptime(day, '%Y-%m-%d')
            except Exception as e:
                self.logger.error(f"Could not decode date {day} for {person['id']}")
                return False

            # Account for leap years (else it would crash the next line with an out of bounds day)
            if bday.month == 2 and bday.day == 29:
                if self.curdate.date() == date(self.curdate.year, 3, 1):
                    return True
            # If the month and day is the same as today then yes
            elif date(self.curdate.year, bday.month, bday.day) == self.curdate.date():
                return True
            break
        else:  # No matching expression?
            self.logger.debug(f"Person {person['id']} has no specified birthday")

        return False

    def has_exception(self, person):
        # No longer works for the company
        # Easy, if it's populated at all then skip
        if person['employmentEndDate'] is not None:
            return True

        # Has not yet started
        for day in re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", person['employmentStartDate']):
            try:  # Dirty date could crash this
                start_date = datetime.strptime(day, '%Y-%m-%d')
            except Exception as e:
                self.logger.error(f"Could not decode date {day} for {person['id']}")
                return False

            # Hasn't started yet
            if start_date > self.curdate:
                return True
            break
        else:
            return True  # No start date specified? Not eligible

        # Specifically excluded, do this check last for efficiency
        exceptions = self.fetch_exceptions()
        if person['id'] in exceptions:
            return True

        return False  # No exceptions hit

    def generate_email(self, person):
        # There's no email on the API, so try fetch the field and then default to the configured mail address
        to_email = person.get('emailAddress', shared_globals.conf.default_to_mail)

        subject = f"Best wishes from {shared_globals.conf.company_name}"
        msg = f"Happy birthday {person['name']} {person['lastname']}"

        return to_email, subject, msg

