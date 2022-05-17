"""
    Chris Thornton 2022-05-16
    Simple class for sharing variables across modules
"""


def init(config):
    global conf
    conf = config

    global is_dev
    is_dev = conf.environment == 'dev'

    if is_dev:
        print("WARNING: running in development environment")
