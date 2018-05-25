"""
Tools to encapsulate generic receive connectors
"""
import logging
import paho.mqtt.client as mqtt

from . import URL, PORT, KEEPALIVE
from ..messager.decorators import decode_message


class Receiver(mqtt.Client):
    """
    Receive messages from specific mqtt queue

    Args:
        topics (list):
            list of strings with the topic names

        processor (Processor):
            processor for received message
    """
    def __init__(self, topics=[], url=None, port=None, keepalive=None):
        super().__init__()
        self.input_topics = topics
        self.processor = processor

        self.connect(
            url or URL,
            port or PORT,
            keepalive or KEEPALIVE
        )

    @staticmethod  # decorator to avoid double 'self' on paho callback
    def on_connect(self, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response
        from the server.
        """
        logging.info(f'Connected with Mosquitto Server: (code) {rc}')
        logging.debug(f'Listen to {map(lambda x: x.name, self.input_topics)}')
        self.listen(self.input_topics)

    @staticmethod  # decorator to avoid double 'self' on paho callback
    def on_message(self, userdata, message):
        """
        The callback for when a PUBLISH message is received from the server.
        """
        self.process(userdata, message)

    def process(self, userdata, message):
        raise NotImplementedError

    def run(self):
        """
        Blocking call that processes network traffic, dispatches callbacks and
        handles reconnecting.
        Other loop*() functions are available that give a threaded interface
        and a manual interface.
        """
        self.running = True
        while self.running:
            self.client.loop()

    def listen(self, topics):
        """
        Subscribe to a list of channels

        Args:
            topics (list):
                list of topics to subscribe the mqtt listener
        """
        for topic in map(lambda x: x.topic, topics):
            try:
                self.client.subscribe(topic.topic)
                logging.debug(f'Subscribed the {topic.topic} topic')
            except:
                logging.debug(f"Can't subscribe the {topic.topic} topic")

    def stop(self):
        """
        Stop running
        """
        self.running = False
