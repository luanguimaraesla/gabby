"""
Gabby module witch creates the Gabby class to handle creation of
message queue nodes for intercommunication
"""
from collections import namedtuple

from .mqtt.transmitter import Transmitter, Receiver
from .messager.decoder import decode
from .messager.message import Message

Topic = namedtuple('Topic', ['name', 'topic', 'fmt'])

class Gabby(Transmitter, Receiver):
    def __init__(self, input_topics, output_topics, decode_input=True,
                 encode_output=True, url=None, port=None, keepalive=None):
        """
        Processor initializer

        Args:
            topics (collection):
                output topics to send results

            decoder (bool), default=True:
                enable auto encoding/decoding of any received message
        """
        Receiver.__init__(self, input_topics, url, port, keepalive)
        Transmitter.__init__(self, name, output_topics, url, port, keepalive)
        self.decode_input = decode_input
        self.encode_output = encode_output

    def process(self, userdata, message):
        if self.decode_input:
            topic_name = message.topic
            topic = filter(lambda x: x.name == topic_name, self.input_topics)
            message = decode(message, topic.fmt)

        response_messages = self.process(message)

        self.send(self.process(message), self.encode_output)

    def transform(self, message):
        """
        Abstract method to process any received message

        Args:
            message (Message or paho.mqtt.MQTTMessage):
                message from queue decoded or not depending on 'decode' var

            author (str):
                message's writer

        Return:
            Collection of messages to be transmitted or an empty list
        """
        return [Message(message.data)]
