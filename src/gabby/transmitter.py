import logging
import paho.mqtt.client as mqtt

from . import URL, PORT, KEEPALIVE
from ..messager.message import Message

class Transmitter(mqtt.Client):
    """
    Handler for MQTT publishing

    Args:
        topics (dict):
            keys identify the topic,s for the mqtt topic
            names to publish
    """
    def __init__(self, topics, url=None, port=None, keepalive=None):
        self.output_topics = topics

        try:
            getattr(self, "connected")
        except AttributeError:
           self.connected = False
        finally:
            if not self.connected:
                self.connect(
                    url or URL,
                    port or PORT,
                    keepalive or KEEPALIVE
                )
                self.connected = True

    @staticmethod
    def on_connect(self, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response
        from the server.
        """
        logging.info(f'Connected with MQTT Server: (code) {rc}')

    def send(self, message):
        """
        Publish string to the 2RSystem queue

        Args:
            data (str):
                string message to publish
            to (str):
                topic name
        """
        receivers = []
        if isinstance(message, Message):
            receivers = message.filter_topics(self.output_topics)

        logging.debug(f"Sending message to {receivers}")

        for topic in map(lambda x: x.topic, receivers):
            logging.info(f'Publishing on topic {topic}')
            self.publish(topic, message.encoded)
