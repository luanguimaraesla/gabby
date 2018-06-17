"""
Tools to encapsulate generic receive connectors
"""
import logging
import time
import mqttsn.client as mqttsn

from .topic import TopicCollection
from .settings import UDP_URL, UDP_PORT
from .decorators import ensure_udp_connection


class UDPReceiver(mqttsn.Client, mqttsn.Callback):
    """
    Receive messages from specific mqttsn broker

    Args:
        topics (list):
            list of strings with the topic names

        url (str):
            mqttsn server url

        port (int):
            mqttsn server port
    """
    def __init__(self, topics=[], url=None, port=None):
        super().__init__(host=url or UDP_URL, port=port or UDP_PORT)
        self.input_topics = TopicCollection(topics)
        self._hack_udp_callbacks()

    def message_arrived(self, topic_name, payload, qos, retained, msg_id):
        """
        Callback to receive messsages
        """
        logging.warning(f'Received UDP message from {topic_name} topic')
        logging.warning(f'Message: {payload}')
        self.process(topic_name, payload)
        return True

    def _hack_udp_callbacks(self):
        # Hack to use callback inside Receiver
        # [FIXME] Should fix at mqttsn project
        self.register_callback(self)

    def process(self, userdata, message):
        raise NotImplementedError

    @ensure_udp_connection
    def run(self):
        """
        Blocking call that processes network traffic, dispatches callbacks and
        handles reconnecting.
        Other loop*() functions are available that give a threaded interface
        and a manual interface.
        """
        self.listen(self.input_topics.filter_by(transmission='udp'))

        logging.info('Getting into the listening loop')
        self.running = True
        while self.running:
            time.sleep(1)

    @ensure_udp_connection
    def listen(self, topics):
        """
        Subscribe to a list of channels

        Args:
            topics (list):
                list of topics to subscribe the mqtt listener
        """
        logging.debug(f'Listen to {list(map(lambda x: x.name, topics))}')

        for topic in map(lambda x: x.name, topics):
            self.subscribe(topic)
            logging.debug(f'Subscribed the {topic} topic')

    def stop(self):
        """
        Stop running
        """
        self.running = False
