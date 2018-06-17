"""
Gabby module witch creates the Gabby class to handle creation of
message queue nodes for intercommunication
"""
import logging

from .udp_transmitter import UDPTransmitter
from .transmitter import Transmitter
from .udp_receiver import UDPReceiver
from .receiver import Receiver
from .message import Message


class Gabby(Transmitter, Receiver, UDPTransmitter, UDPReceiver):
    def __init__(self, input_topics=None, output_topics=None, decode_input=True,
                 url=None, port=None, keepalive=None, udp_url=None,
                 udp_port=None, transmission='tcp'):
        """
        Gabby object initializer

        Args:
            input_topics (collection):
                output topics to send results

            decoder (bool), default=True:
                enable auto encoding/decoding of any received message
        """
        Receiver.__init__(self, input_topics or [], url, port, keepalive)
        Transmitter.__init__(self, output_topics or [], url, port, keepalive)
        UDPReceiver.__init__(self, input_topics or [], udp_url, udp_port)
        UDPTransmitter.__init__(self, output_topics or [], udp_url, udp_port)
        self.decode_input = decode_input
        self.transmission = transmission

    def process(self, userdata, message):
        if self.decode_input:
            topic_name = message.topic
            topics = self.input_topics.filer_by(name=topic_name)
            message = Message.decode(message.payload, topics)

        logging.debug(f'Processing message: {message}')
        response_messages = self.transform(message)
        for msg in response_messages:
            self.send(msg)

    def transform(self, message):
        """
        Abstract method to process any received message

        Args:
            message (Message or paho.mqtt.MQTTMessage):
                message from queue decoded or not depending on 'decode' var

        Return:
            Collection of messages to be transmitted, an empty list, or None
        """
        return [Message(message.data, self.output_topics)]

    def run(self):
        """
        Runner handler for both transmission protocols
        """
        if isinstance(self.transmission, (list, tuple)):
            if 'tcp' in self.transmission and 'udp' in self.transmission:
                UDPReceiver.run(self, join=False)
                Receiver.run(self)
            elif 'tcp' in self.transmission:
                Receiver.run(self)
            elif 'udp' in self.transmission:
                UDPReceiver.run(self)
        elif isinstance(self.transmission, str):
            if self.transmission == 'tcp':
                UDPReceiver.run(self)
            elif self.transmission == 'udp':
                UDPReceiver.run(self)
        else:
            raise AttributeError('transmission attr should be str or list')
