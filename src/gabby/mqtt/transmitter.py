import paho.mqtt.client as mqtt
from . import URL, PORT, KEEPALIVE

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
        self.connect(
            url or URL,
            port or PORT,
            keepalive or KEEPALIVE
        )

    def on_connect(self, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response
        from the server.
        """
        logging.info(f'Connected with MQTT Server: (code) {rc}')

    def send(self, message, encode_message):
        """
        Publish string to the 2RSystem queue

        Args:
            data (str):
                string message to publish
            to (str):
                topic name
        """
        receivers = []
        if encode_message:
            receivers = filter(
                lambda x: x.name == message.to,
                self.output_topics
            )
        receivers = receivers or self.output_topics

        for topic in map(lambda x: x.topic, receivers):
            logging.info(f'Publishing on topic {self.topics}')
            self.publish(topic, message)
