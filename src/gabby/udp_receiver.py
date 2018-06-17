"""
Tools to encapsulate generic receive connectors
"""
import logging
import types
import time
import mqttsn.client as mqttsn

from .topic import TopicCollection
from .settings import UDP_URL, UDP_PORT


class UDPReceiver(mqttsn.Client):
    """
    Receive messages from specific mqtt queue

    Args:
        topics (list):
            list of strings with the topic names

        url (str):
            mqtt server url

        port (int):
            mqtt server port

        keepalive (int):
            mqtt keepalive time in seconds
    """
    def __init__(self, topics=[], url=None, port=None):
        super().__init__(host=url or UDP_URL, port=port or UDP_PORT)
        self.input_topics = TopicCollection(topics)
        self._register_udp_callbacks()

    @staticmethod
    def message_arrived(self, topic_name, payload, qos, retained, msg_id):
        logging.warning(f'Received UDP message from {topic_name} topic')
        logging.warning(f'Message: {payload}')
        self.process(topic_name, payload)
        return True

    def _register_udp_callbacks(self):
        callback = mqttsn.Callback()
        callback.message_arrived = \
            types.MethodType(UDPReceiver.message_arrived, callback)
        self.register_callback(callback)

    def process(self, userdata, message):
        raise NotImplementedError

    def run(self):
        """
        Blocking call that processes network traffic, dispatches callbacks and
        handles reconnecting.
        Other loop*() functions are available that give a threaded interface
        and a manual interface.
        """
        self.listen(self.input_topics)

        logging.info('Getting into the listening loop')
        self.running = True
        while self.running:
            time.sleep(1)

    def listen(self, topics):
        """
        Subscribe to a list of channels

        Args:
            topics (list):
                list of topics to subscribe the mqtt listener
        """
        logging.debug(f'Listen to {list(map(lambda x: x.name, topics))}')

        try:
            getattr(self, "connected")
        except AttributeError:
            self.connected = False
        finally:
            if not self.connected:
                self.connect()
                self.connected = True

        for topic in map(lambda x: x.name, topics):
                self.subscribe(topic)
                logging.debug(f'Subscribed the {topic} topic')

    def stop(self):
        """
        Stop running
        """
        self.running = False
