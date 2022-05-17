"""
    Christopher Thornton
    2022-05-16
"""
import os
from time import sleep
from config import Config
import lib.shared_globals as shared_globals
from lib.utils import DummyLogger

from lib.birthday import BirthdaySender

# Either dev or production, production by default
# If it's a development environment we look at the dummy data instead of the API
environment = os.environ.get('ENVIRONMENT', 'production')

# Initial configuration and initialisation
config = Config(environment)
shared_globals.init(config)
logger = DummyLogger()  # Can set this to a more advanced logger that implements the same methods

if __name__ == '__main__':
    # Can simply create more senders and add to this list for execution
    senders = [
        BirthdaySender(logger)
    ]
    while True:
        # Execute the various senders here
        for sender in senders:
            sender.execute()

        sleep(1800)  # Doesn't need to run often
