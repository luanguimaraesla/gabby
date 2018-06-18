"""
Gabby module witch creates the Gabby class to handle creation of
message queue nodes for intercommunication
"""
import logging
from collections import namedtuple

from .udp_transmitter import UDPTransmitter
from .transmitter import Transmitter
from .udp_receiver import UDPReceiver
from .receiver import Receiver
from .message import Message


Connection = namedtuple('Connection', ['host', 'port', 'options'])


class TCPGabby(self, input_topics=None, output_topics=None, decode_input


class Gabby:
    def __init__(self, input_topics=None, output_topics=None, decode_input=True,
                 url=None, port=None, keepalive=None, udp_url=None,
                 udp_port=None, transmission='tcp'):

        self.connections = {
            'tcp': Connection(url, port, (keepalive,)),
            'udp': Connection(udp_url, udp_port, None),
        }

        self.transmission = \
            [transmission] if isinstance(transmission, str) else transmission

        self.receivers = {}
        self.tcp_receiver = \
            Receiver(input_topics or [], url, port)
        self.tcp_transmitter = \
            Transmitter(output_topics or [], url, port)
        self.udp_receiver = \
            UDPReceiver(input_topics or [], udp_url, udp_port)
        self.udp_transmitter = \
            UDPTransmitter(output_topics or [], udp_url, udp_port)

        self.decode_input = decode_input
        self.transmission = transmission

    def _init_receivers(self, input_topics):
        self.receivers = {}

        if 'tcp' in self.transmission:
            conn = self.connections['tcp']
            self.receivers['tcp'] = Receiver(
                input_topics, conn.url, conn.port, *conn.options
            )
        if 'udp' in self.transmission:
            conn = self.connections['udp']
            self.receivers['udp'] = UDPReceiver(
                input_topics, conn.url, conn.port
            )

    def _init_transmitters(self, output_topics):
        self.receivers = {}

        if 'tcp' in self.transmission:
            conn = self.connections['tcp']
            self.receivers['tcp'] = Receiver(
                input_topics, conn.url, conn.port, *conn.options
            )
        if 'udp' in self.transmission:
            conn = self.connections['udp']
            self.receivers['udp'] = UDPReceiver(
                input_topics, conn.url, conn.port
            )

    def process(self, userdata, message):
        if self.decode_input:
            topic_name = message.topic
            topics = self.input_topics.filter_by(name=topic_name)
            message = Message.decode(message.payload, topics)

        logging.debug(f'Processing message: {message}')
        response_messages = self.transform(message) or []
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
                Receiver.run(self)
            elif self.transmission == 'udp':
                UDPReceiver.run(self)
        else:
            raise AttributeError('transmission attr should be str or list')

    def send(self, message):
        self._dispach(self.transmission, {
            'tcp': Transmitter.send,
            'udp': UDPTransmitter.send
        }, message)

    def _dispach(self, attr, funcs):
        """
        Method to handle func dispach to multiple classes according to
        any attribute
        """
        if isinstance(attr, (list, tuple)):
            which = {k: k in attr for k in funcs.keys()}

        elif isinstance(attr, str):
            which = {k: (k == attr) for k in funcs.keys()}

        for k, func in funcs.items():
            if which[k] is True:
                func[0](**func[1])
