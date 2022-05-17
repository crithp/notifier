"""
    Chris Thornton 2022-05-16
"""
from datetime import datetime


class DummyLogger:
    """
        In place until a proper logging unit is implemented
    """
    def __init__(self):
        pass

    def error(self, message: str):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {message}")

    def debug(self, message: str):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - DEBUG: {message}")

    def critical(self, message: str):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - CRITICAL: {message}")

    def info(self, message: str):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - INFO: {message}")

    def warn(self, message: str):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - WARNING: {message}")

    def warning(self, message: str):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - WARNING: {message}")
