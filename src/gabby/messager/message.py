
"""
Module to handle message serialization
"""
import logging

class Message:
    def __init__(self, data, author=None, to=None):
        logging.debug(f'Creating a new message with this data: {data}')
        message.data = data
        message.to = to

    def __str__(self):
        return str(self.data)
