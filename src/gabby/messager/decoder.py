import struct
import logging

from .message import Message

def decode(message, fmt):
    """
    Convert an MQTTMessage to a Message

    Args:
        message (MQTTMessage):
            A paho.mqtt.MQTTMessage received from any message queue
    """
    data = struct.unpack(fmt, message.payload)
    logging.debug(f'Decoded data: {data}')
    return Message(data)
