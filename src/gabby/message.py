
"""
Module to handle message serialization
"""
import logging
import struct


class Message:
    """
    Handler for struct encoding data
    """
    def __init__(self, data, topics=[], fmt=None):
        logging.debug(f'Creating a new message with this data: {data}')
        self.data = data
        self.topics = topics
        self.fmt = topics[0].fmt if topics else fmt

        if self.fmt is None:
            raise ValueError("You should setup the topic or the fmt")

    @property
    def encoded(self):
        return struct.pack(self.fmt, *self.data)

    def __str__(self):
        return str(self.data)

    def filter_topics(self, topics):
        if not self.topics:
            return filter(lambda x: x.fmt == self.fmt, topics)
        else:
            return filter(lambda x: x in self.topics, topics)

    @staticmethod
    def decode(message, topics=[], fmt=None):
        """
        Convert an MQTTMessage to a Message

        Args:
            message (MQTTMessage):
                A paho.mqtt.MQTTMessage received from any message queue

            topics (collection):
                list of topics to extract fmt of the first topic

            fmt (str):
                struct model of encoded message
        """
        if fmt or topics:
            data = struct.unpack(topics[0].fmt if topics else fmt, message)
            logging.debug(f'Decoded data: {data}')
            return Message(data, topics=topics, fmt=fmt)
        else:
            raise ValueError("You should setup the topic or the fmt")
